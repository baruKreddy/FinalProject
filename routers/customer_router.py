from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from init_db import get_db_conn  
from models.Customer import Customer

router = APIRouter()

@router.post("/customers", response_model=Customer)
def create_customer(customer: Customer,conn: sqlite3.Connection = Depends(get_db_conn)):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
        conn.commit()
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers/{customer_id}")
def read_customer(customer_id: int, conn: sqlite3.Connection = Depends(get_db_conn)):
    try:
       
        c = conn.cursor()
        c.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = c.fetchone()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return {"id": customer[0], "name": customer[1], "phone": customer[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, conn: sqlite3.Connection = Depends(get_db_conn)):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        return {"message": "Customer deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: Customer, conn: sqlite3.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    # Check if the customer exists
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    existing_customer = cursor.fetchone()
    if not existing_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    try:
        # Update the customer in the database
        cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, customer_id))
        conn.commit()
        # Fetch the updated customer details and return them
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        updated_customer = cursor.fetchone()
        return {"id": customer_id, "name": updated_customer[1], "phone": updated_customer[2]}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))