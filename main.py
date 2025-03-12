import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_lottie import st_lottie

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your MySQL password if required
        database="lmanage"
    )

# Function to Add a Book
def add_book():
    st.subheader("📚 Add New Book")
    bname = st.text_input("Enter Book Name")
    bcode = st.text_input("Enter Book Code")
    total = st.number_input("Total Copies", min_value=1, step=1)
    sub = st.text_input("Enter Subject")

    if st.button("Add Book"):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO books (bname, bcode, total, subject) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (bname, bcode, total, sub))
        conn.commit()
        conn.close()
        st.success("✅ Book Added Successfully!")

# Function to Issue a Book
def issue_book():
    st.subheader("📖 Issue a Book")
    name = st.text_input("Student Name")
    regno = st.text_input("Registration Number")
    bcode = st.text_input("Book Code")
    date = st.date_input("Issue Date")

    if st.button("Issue Book"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT total FROM books WHERE bcode = %s", (bcode,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            cursor.execute("INSERT INTO issue (name, regno, bcode, idate) VALUES (%s, %s, %s, %s)",
                           (name, regno, bcode, date))
            cursor.execute("UPDATE books SET total = total - 1 WHERE bcode = %s", (bcode,))
            conn.commit()
            st.success(f"✅ Book Issued to {name} Successfully!")
        else:
            st.error("❌ Book Not Available!")

        conn.close()

# Function to Submit a Book
def submit_book():
    st.subheader("📦 Submit a Book")
    name = st.text_input("Student Name")
    regno = st.text_input("Registration Number")
    bcode = st.text_input("Book Code")
    sdate = st.date_input("Submission Date")

    if st.button("Submit Book"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO submit (name, regno, bcode, sdate) VALUES (%s, %s, %s, %s)",
                       (name, regno, bcode, sdate))
        cursor.execute("UPDATE books SET total = total + 1 WHERE bcode = %s", (bcode,))
        conn.commit()
        conn.close()
        st.success("✅ Book Submitted Successfully!")

# Function to Delete a Book
def delete_book():
    st.subheader("🗑️ Delete a Book")
    bcode = st.text_input("Enter Book Code to Delete")

    if st.button("Delete Book"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE bcode = %s", (bcode,))
        conn.commit()
        conn.close()
        st.warning("✅ Book Deleted Successfully!")

# Function to Display Books
def display_books():
    st.subheader("📚 Available Books")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    if books:
        df = pd.DataFrame(books, columns=["Book Name", "Book Code", "Total Copies", "Subject"])
        st.dataframe(df)
    else:
        st.warning("No Books Available!")

# Main Function to Display Options
def main():
    st.title("📖 Library Management System")
    st.sidebar.title("📌 Menu")

    options = ["Home", "Add Book", "Issue Book", "Submit Book", "Delete Book", "View Books"]
    choice = st.sidebar.radio("Select an Option", options)

    if choice == "Home":
        st.image("https://cdn.pixabay.com/photo/2017/09/22/19/06/old-books-2776228_960_720.jpg", use_column_width=True)
        st.write("📚 **Welcome to the Library Management System!**")

    elif choice == "Add Book":
        add_book()

    elif choice == "Issue Book":
        issue_book()

    elif choice == "Submit Book":
        submit_book()

    elif choice == "Delete Book":
        delete_book()

    elif choice == "View Books":
        display_books()

# Run the Streamlit App
if __name__ == "__main__":
    main()
