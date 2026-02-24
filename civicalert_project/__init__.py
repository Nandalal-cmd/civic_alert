import pymysql

# This tricks Django into thinking mysqlclient is installed and up to date
pymysql.version_info = (2, 2, 7, "final", 0) 
pymysql.install_as_MySQLdb()