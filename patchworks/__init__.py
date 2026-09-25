import pymysql

# Permite que o Django use PyMySQL no lugar do mysqlclient
pymysql.install_as_MySQLdb()
