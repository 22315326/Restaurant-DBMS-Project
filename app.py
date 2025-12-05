import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Restaurant Management System", layout="wide")

# 1. Initialize Supabase Connection
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_connection()

# 2. Authentication Logic
def login_user(username, password):
    try:
        response = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
        if len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Login Error: {e}")
        return None

# 3. Data Functions (GET)
def get_menu_items():
    try:
        response = supabase.table("menuitems").select("*, categories(category_name)").order("item_id").execute()
        if response.data:
            items = []
            for item in response.data:
                flat_item = {
                    "ID": item["item_id"],
                    "Name": item["item_name"],
                    "Price": float(item["price"]),
                    "Category": item["categories"]["category_name"] if item["categories"] else "Unknown",
                    "Available": item["is_available"]
                }
                items.append(flat_item)
            return pd.DataFrame(items)
    except Exception as e:
        st.error(f"Data Fetch Error: {e}")
    return pd.DataFrame()

def get_tables():
    try:
        response = supabase.table("restauranttables").select("*").order("table_id").execute()
        return response.data
    except Exception as e:
        st.error(f"Table Fetch Error: {e}")
        return []

# 4. Action Functions (INSERT/DELETE)
def add_menu_item(name, description, price, category_id):
    try:
        data = {"item_name": name, "description": description, "price": price, "category_id": category_id}
        supabase.table("menuitems").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Insert Error: {e}")
        return False

def delete_menu_item(item_id):
    try:
        supabase.table("menuitems").delete().eq("item_id", item_id).execute()
        return True
    except Exception as e:
        st.error(f"Delete Error: {e}")
        return False

def place_order(table_id, user_id, cart_items, total_amount):
    try:
        # 1. Create Order Record
        order_data = {
            "table_id": table_id,
            "user_id": user_id,
            "total_amount": total_amount,
            "status": "Pending",
            "order_date": datetime.now().isoformat()
        }
        order_res = supabase.table("orders").insert(order_data).execute()
        
        if not order_res.data:
            st.error("Failed to create order.")
            return False
            
        new_order_id = order_res.data[0]['order_id']
        
        # 2. Create Order Details Records
        details_data = []
        for item in cart_items:
            details_data.append({
                "order_id": new_order_id,
                "item_id": item['id'],
                "quantity": item['quantity'],
                "unit_price": item['price']
            })
            
        supabase.table("orderdetails").insert(details_data).execute()
        return True
    except Exception as e:
        st.error(f"Order Placement Error: {e}")
        return False

# 5. Session State Init
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 6. Main Interface
if not st.session_state['logged_in']:
    # --- LOGIN SCREEN ---
    st.title("Restaurant DBMS Login")
    col1, col2 = st.columns([1, 2])
    with col1:
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        login_btn = st.button("Login", type="primary")

    if login_btn:
        user = login_user(username_input, password_input)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user_info'] = user
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

else:
    # --- DASHBOARD ---
    user_info = st.session_state['user_info']
    
    # Sidebar
    st.sidebar.title(f"User: {user_info['full_name']}")
    menu_choice = st.sidebar.radio("Navigation", ["Menu Management", "New Order", "Active Orders"])
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['cart'] = []
        st.rerun()

    # --- MENU MODULE ---
    if menu_choice == "Menu Management":
        st.header("Menu Management")
        df_menu = get_menu_items()
        st.dataframe(df_menu, use_container_width=True)
        st.divider()
        
        col_add, col_del = st.columns(2)
        with col_add:
            st.subheader("Add Item")
            with st.form("add_item"):
                name = st.text_input("Name")
                price = st.number_input("Price", min_value=0.0)
                cat = st.selectbox("Category", ["Main Course (1)", "Beverages (2)", "Desserts (3)"])
                if st.form_submit_button("Add"):
                    cat_id = int(cat.split('(')[1].replace(')', ''))
                    if add_menu_item(name, "desc", price, cat_id):
                        st.success("Added!")
                        st.rerun()
        with col_del:
            st.subheader("Delete Item")
            del_id = st.number_input("ID to Delete", min_value=1)
            if st.button("Delete"):
                if delete_menu_item(del_id):
                    st.success("Deleted!")
                    st.rerun()

    # --- NEW ORDER MODULE ---
    elif menu_choice == "New Order":
        st.header("Create New Order")
        
        # Step 1: Select Table
        tables = get_tables()
        table_options = {t['table_number']: t['table_id'] for t in tables}
        selected_table_name = st.selectbox("Select Table", list(table_options.keys()))
        
        st.divider()
        
        # Step 2: Add Items to Cart
        col_menu, col_cart = st.columns([1, 1])
        
        with col_menu:
            st.subheader("Menu")
            df_menu = get_menu_items()
            
            # Selection Form
            with st.form("add_to_cart"):
                # Create a list of names for the dropdown
                item_list = df_menu['Name'].tolist() if not df_menu.empty else []
                selected_item_name = st.selectbox("Select Item", item_list)
                quantity = st.number_input("Quantity", min_value=1, value=1)
                
                add_btn = st.form_submit_button("Add to Cart")
                
                if add_btn and not df_menu.empty:
                    # Find details of selected item
                    selected_row = df_menu[df_menu['Name'] == selected_item_name].iloc[0]
                    item_details = {
                        "id": int(selected_row['ID']),
                        "name": selected_item_name,
                        "price": float(selected_row['Price']),
                        "quantity": quantity,
                        "total": quantity * float(selected_row['Price'])
                    }
                    st.session_state['cart'].append(item_details)
                    st.success(f"{quantity} x {selected_item_name} added!")
        
        # Step 3: Review Cart & Submit
        with col_cart:
            st.subheader("Current Order (Cart)")
            if len(st.session_state['cart']) > 0:
                cart_df = pd.DataFrame(st.session_state['cart'])
                st.dataframe(cart_df[['name', 'quantity', 'price', 'total']], use_container_width=True)
                
                grand_total = cart_df['total'].sum()
                st.markdown(f"### Total: ${grand_total:.2f}")
                
                # Buttons
                c1, c2 = st.columns(2)
                if c1.button("Clear Cart"):
                    st.session_state['cart'] = []
                    st.rerun()
                    
                if c2.button("Submit Order", type="primary"):
                    table_id = table_options[selected_table_name]
                    user_id = user_info['user_id']
                    
                    if place_order(table_id, user_id, st.session_state['cart'], grand_total):
                        st.success("Order placed successfully!")
                        st.session_state['cart'] = [] # Reset cart
                        st.rerun()
            else:
                st.info("Cart is empty.")

    # --- ACTIVE ORDERS MODULE (VIEW ONLY) ---
    elif menu_choice == "Active Orders":
        st.header("Active Orders")
        # Simple Join Query to show orders
        try:
            # Fetch orders with table info
            res = supabase.table("orders").select("*, restauranttables(table_number), users(username)").order("order_date", desc=True).execute()
            
            if res.data:
                # Format for display
                display_data = []
                for o in res.data:
                    display_data.append({
                        "Order ID": o['order_id'],
                        "Table": o['restauranttables']['table_number'],
                        "Waiter": o['users']['username'],
                        "Date": o['order_date'].split('T')[0],
                        "Total": o['total_amount'],
                        "Status": o['status']
                    })
                st.dataframe(pd.DataFrame(display_data), use_container_width=True)
            else:
                st.info("No orders found.")
        except Exception as e:
            st.error(f"Error fetching orders: {e}")