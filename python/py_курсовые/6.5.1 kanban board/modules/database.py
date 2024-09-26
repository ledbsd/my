"""Working with database server"""
from os import getenv
import psycopg2


class DBServer():
    """Work with Postgres database"""
    def __init__(self):
        self.__hostname = 'localhost'
        self.__port = 5432
        self.__dbname = 'postgres'
        self.__user = getenv('DB_USERNAME')
        self.__password = getenv('DB_PASSWORD')

    @property
    def cred_params(self):
        """Getting credentials as params"""
        return {
            'dbname': self.__dbname,
            'port': self.__port,
            'host': self.__hostname,
            'user': self.__user,
            'password': self.__password
        }

    def get_metric_from_db(self):
        """"
        Getting metrics from DB
        :return: team data in the same format as the data from the monitoring server via http
        """
        team_data = ''

        try:
            with psycopg2.connect(**self.cred_params) as dbconnect:
                with dbconnect.cursor() as cursor:
                    cursor.execute(R"""
                        select team
                        from usage_stats.resources
                        group by team
                    """)

                    team_list = cursor.fetchall()
                    dbconnect.commit()

                    for team in team_list:
                        if team_data != '':
                            team_data += '$'
                        team_data = team_data + team[0] + '|'
                        cursor.execute(R"""
                            select resource,dimension,CAST(collect_date AS VARCHAR),usage
                            from usage_stats.resources
                            where team = %s
                            order by team
                        """, [team[0]])
                        resource_data = ';'.join(str(resource_id) for resource_id in cursor.fetchall())
                        team_data = team_data + resource_data.replace(', ', ',').replace('\'', '')
                        dbconnect.commit()

        except psycopg2.OperationalError:
            print('Connection to DB was failed')

        return team_data
