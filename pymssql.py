{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "2c20c10f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: pymssql in ./anaconda3/lib/python3.11/site-packages (2.2.8)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install pymssql\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "feafe4fe",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pymssql"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "942b84da",
   "metadata": {},
   "outputs": [
    {
     "ename": "OperationalError",
     "evalue": "(20009, b'DB-Lib error message 20009, severity 9:\\nUnable to connect: Adaptive Server is unavailable or does not exist (ORA_Safety.sql.insideaag.com,1450)\\n')",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mMSSQLDatabaseException\u001b[0m                    Traceback (most recent call last)",
      "File \u001b[0;32msrc/pymssql/_pymssql.pyx:647\u001b[0m, in \u001b[0;36mpymssql._pymssql.connect\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32msrc/pymssql/_mssql.pyx:2109\u001b[0m, in \u001b[0;36mpymssql._mssql.connect\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32msrc/pymssql/_mssql.pyx:701\u001b[0m, in \u001b[0;36mpymssql._mssql.MSSQLConnection.__init__\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32msrc/pymssql/_mssql.pyx:1818\u001b[0m, in \u001b[0;36mpymssql._mssql.maybe_raise_MSSQLDatabaseException\u001b[0;34m()\u001b[0m\n",
      "File \u001b[0;32msrc/pymssql/_mssql.pyx:1835\u001b[0m, in \u001b[0;36mpymssql._mssql.raise_MSSQLDatabaseException\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;31mMSSQLDatabaseException\u001b[0m: (20009, b'DB-Lib error message 20009, severity 9:\\nUnable to connect: Adaptive Server is unavailable or does not exist (ORA_Safety.sql.insideaag.com,1450)\\n')",
      "\nDuring handling of the above exception, another exception occurred:\n",
      "\u001b[0;31mOperationalError\u001b[0m                          Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[3], line 6\u001b[0m\n\u001b[1;32m      3\u001b[0m Username \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mSafetyME\u001b[39m\u001b[38;5;124m'\u001b[39m\n\u001b[1;32m      4\u001b[0m Password \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mShakennotstirred1!\u001b[39m\u001b[38;5;124m'\u001b[39m\n\u001b[0;32m----> 6\u001b[0m conn \u001b[38;5;241m=\u001b[39m pymssql\u001b[38;5;241m.\u001b[39mconnect(server\u001b[38;5;241m=\u001b[39mServer,user\u001b[38;5;241m=\u001b[39mUsername,password\u001b[38;5;241m=\u001b[39mPassword,database\u001b[38;5;241m=\u001b[39mDatabase)\n",
      "File \u001b[0;32msrc/pymssql/_pymssql.pyx:653\u001b[0m, in \u001b[0;36mpymssql._pymssql.connect\u001b[0;34m()\u001b[0m\n",
      "\u001b[0;31mOperationalError\u001b[0m: (20009, b'DB-Lib error message 20009, severity 9:\\nUnable to connect: Adaptive Server is unavailable or does not exist (ORA_Safety.sql.insideaag.com,1450)\\n')"
     ]
    }
   ],
   "source": [
    "Server = 'ORA_Safety.sql.insideaag.com,1450'\n",
    "Database = 'Safety'\n",
    "Username = 'SafetyME'\n",
    "Password = 'Shakennotstirred1!'\n",
    "\n",
    "conn = pymssql.connect(server=Server,user=Username,password=Password,database=Database)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7f75be3b",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
