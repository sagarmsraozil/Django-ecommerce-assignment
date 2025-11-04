"""
Analytics module for e-commerce platform
This file contains intentional code patterns for SonarQube analysis
"""
import datetime
from decimal import Decimal


class SalesAnalytics:
    """Analytics for sales data"""
    
    def __init__(self):
        self.sales_data = []
        self.customer_data = []
        self.product_data = []
    
    def calculate_total_revenue(self, orders):
        """Calculate total revenue from orders"""
        total = 0
        for order in orders:
            for item in order.items:
                total = total + item.price * item.quantity
        return total
    
    def calculate_average_order_value(self, orders):
        """Calculate average order value"""
        total = 0
        count = 0
        for order in orders:
            for item in order.items:
                total = total + item.price * item.quantity
            count = count + 1
        if count == 0:
            return 0
        return total / count
    
    def get_top_products(self, orders, limit=10):
        """Get top selling products"""
        product_sales = {}
        for order in orders:
            for item in order.items:
                if item.product_id in product_sales:
                    product_sales[item.product_id] = product_sales[item.product_id] + item.quantity
                else:
                    product_sales[item.product_id] = item.quantity
        
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:limit]
    
    def get_customer_lifetime_value(self, customer_id, orders):
        """Calculate customer lifetime value"""
        total = 0
        for order in orders:
            if order.customer_id == customer_id:
                for item in order.items:
                    total = total + item.price * item.quantity
        return total
    
    def generate_monthly_report(self, year, month):
        """Generate monthly sales report"""
        # This is a long method that should be refactored (code smell)
        report = {}
        report['total_orders'] = 0
        report['total_revenue'] = 0
        report['total_customers'] = 0
        report['new_customers'] = 0
        report['returning_customers'] = 0
        report['average_order_value'] = 0
        report['top_products'] = []
        report['top_customers'] = []
        report['daily_sales'] = {}
        
        # Complex nested logic
        for day in range(1, 32):
            try:
                date = datetime.date(year, month, day)
                report['daily_sales'][str(date)] = 0
            except:
                pass
        
        return report
    
    def process_refunds(self, order_id, items):
        """Process refund for order items"""
        refund_amount = 0
        for item in items:
            refund_amount = refund_amount + item.price * item.quantity
        return refund_amount


class CustomerAnalytics:
    """Analytics for customer behavior"""
    
    def __init__(self):
        self.customer_segments = []
    
    def segment_customers(self, customers):
        """Segment customers based on purchase behavior"""
        segments = {
            'high_value': [],
            'medium_value': [],
            'low_value': [],
            'inactive': []
        }
        
        for customer in customers:
            total_spent = 0
            for order in customer.orders:
                for item in order.items:
                    total_spent = total_spent + item.price * item.quantity
            
            if total_spent > 1000:
                segments['high_value'].append(customer)
            elif total_spent > 500:
                segments['medium_value'].append(customer)
            elif total_spent > 100:
                segments['low_value'].append(customer)
            else:
                segments['inactive'].append(customer)
        
        return segments
    
    def calculate_churn_rate(self, customers, days=90):
        """Calculate customer churn rate"""
        # Duplicated logic from above
        total_customers = len(customers)
        inactive_customers = 0
        
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        for customer in customers:
            last_order_date = None
            for order in customer.orders:
                if last_order_date is None or order.created_at > last_order_date:
                    last_order_date = order.created_at
            
            if last_order_date is None or last_order_date < cutoff_date:
                inactive_customers = inactive_customers + 1
        
        if total_customers == 0:
            return 0
        
        return (inactive_customers / total_customers) * 100


class ProductAnalytics:
    """Analytics for product performance"""
    
    def analyze_product_performance(self, product_id, orders):
        """Analyze individual product performance"""
        metrics = {
            'total_sold': 0,
            'total_revenue': 0,
            'average_price': 0,
            'return_rate': 0
        }
        
        # Duplicated calculation logic
        for order in orders:
            for item in order.items:
                if item.product_id == product_id:
                    metrics['total_sold'] = metrics['total_sold'] + item.quantity
                    metrics['total_revenue'] = metrics['total_revenue'] + (item.price * item.quantity)
        
        if metrics['total_sold'] > 0:
            metrics['average_price'] = metrics['total_revenue'] / metrics['total_sold']
        
        return metrics
    
    def get_product_recommendations(self, product_id, all_orders):
        """Get product recommendations based on purchase history"""
        # Complex logic that could be simplified
        related_products = {}
        
        for order in all_orders:
            has_product = False
            order_products = []
            
            for item in order.items:
                order_products.append(item.product_id)
                if item.product_id == product_id:
                    has_product = True
            
            if has_product:
                for prod_id in order_products:
                    if prod_id != product_id:
                        if prod_id in related_products:
                            related_products[prod_id] = related_products[prod_id] + 1
                        else:
                            related_products[prod_id] = 1
        
        sorted_recommendations = sorted(related_products.items(), key=lambda x: x[1], reverse=True)
        return sorted_recommendations[:5]


def calculate_discount_amount(price, discount_percentage):
    """Calculate discount amount - simple utility function"""
    return price * (discount_percentage / 100)


def calculate_tax(amount, tax_rate):
    """Calculate tax amount - simple utility function"""
    return amount * (tax_rate / 100)


def calculate_final_price(price, discount_percentage, tax_rate):
    """Calculate final price after discount and tax"""
    # Could use the above functions but doesn't (code smell)
    discount = price * (discount_percentage / 100)
    price_after_discount = price - discount
    tax = price_after_discount * (tax_rate / 100)
    final_price = price_after_discount + tax
    return final_price