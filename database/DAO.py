from database.DB_connect import DBConnect
from model.product import Product


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT Date
                            FROM go_sales.go_daily_sales"""
        cursor.execute(query, )
        for row in cursor:
            if row['Date'].year not in result:
                result.append(row['Date'].year)

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllColor():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT Product_color
                        FROM go_products
                        WHERE Product_color != 'Unspecified'
                        ORDER BY Product_color"""
        cursor.execute(query, )
        for row in cursor:
            result.append(row['Product_color'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProduct(color):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM go_products
                    WHERE Product_color = %s"""
        cursor.execute(query, (color,))
        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getConnection(anno, colore):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.P1, t.P2, COUNT(DISTINCT (t.`Date`)) as COUNT
                    from (SELECT g1.Retailer_code as R1, g2.`Date`, g1.Product_number as P1, g2.Product_number as P2
                            from (select gds1.Retailer_code, gp1.Product_number, gds1.`Date`
                                    from go_daily_sales gds1, go_products gp1
                                    where gp1.Product_number = gds1.Product_number and gp1.Product_color = %s) g1,
                                (select gds2.Retailer_code, gp2.Product_number, gds2.`Date`
                                    from go_daily_sales gds2, go_products gp2
                                    where gp2.Product_number = gds2.Product_number and gp2.Product_color = %s) g2
                            where g1.`Date` = g2.`Date` and g1.Retailer_code = g2.Retailer_code and 
                                  g1.Product_number < g2.Product_number and EXTRACT(year from g2.`Date`) = %s) t
                    group by t.P1, t.P2"""
        cursor.execute(query, (colore,colore,anno,))
        for row in cursor:
            result.append((row['P1'],
                          row['P2'],
                          row['COUNT']))

        cursor.close()
        conn.close()
        return result