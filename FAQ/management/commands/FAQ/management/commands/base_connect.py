import pymysql
from AdminForFAQ.settings import DATABASES


class DBConnector:
    """SQL запросы к базе данных"""

    def __init__(self):
        """Подключение к базе данных"""
        self.connection = pymysql.connect(host=DATABASES['default']['HOST'],
                                          user=DATABASES['default']['USER'],
                                          password=DATABASES['default']['PASSWORD'],
                                          db=DATABASES['default']['NAME'],
                                          charset='utf8mb4',
                                          )

    def get_bot_tokens(self):
        """Получение токенов"""
        query = """ SELECT token
                    FROM 
      FAQ_settingsbot
                    """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            tokens_set = {token[0] for token in cursor.fetchall()}
            return tokens_set

class BotQueries(DBConnector):
    """Запросы экземпляров бота"""

    def __init__(self, token):
        super().__init__()
        self.bot_id = self.get_bot_id(token)

    def get_bot_id(self, token):
        """Получение ID бота"""
        query = """select id
                    FROM 
      FAQ_settingsbot
                    WHERE token=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (token,))
            bot_id = cursor.fetchone()[0]
            return bot_id

    def get_all_questions(self):
        """Получение вопросов"""
        query = """ SELECT id, question, answer, general 
                    FROM 
      FAQ_questions
                    WHERE bot_id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            question_data = cursor.fetchall()
            questions = {data[0]: (data[1], data[2], data[3]) for data in question_data}
            return questions

    def get_questions_relations(self):
        """Получение связей вопросов"""
        query = """ SELECT base_id, sub_id
                    FROM 
      FAQ_relationquestion as rq 
                    LEFT JOIN 
      FAQ_questions as qu
                    ON qu.id = rq.sub_id
                    WHERE bot_id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            relations = list(cursor.fetchall())
            return relations

    def get_last_update(self):
        """Дата последнего изменения в базе"""
        query = """ SELECT upd.bot_id, max(upd.updated) as last_update
                    FROM 
                        (   SELECT q.bot_id AS bot_id, max(rq.updated) AS updated
                            FROM 
      FAQ_relationquestion as rq  left join 
      FAQ_questions as q
                            ON rq.base_id = q.id
                            GROUP BY q.bot_id
                            union
                            SELECT id , max(updated)
                            FROM 
      FAQ_settingsbot
                            GROUP BY id
                            union
                            SELECT bot_id, max(updated)
                            FROM 
      FAQ_questions
                            GROUP BY bot_id) as upd
                    WHERE bot_id=%s
                    """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            last_update = cursor.fetchall()[0][1]
            return last_update

    def get_settings_bot(self):
        """Настройки бота"""
        query = """ SELECT  title_question, 
                            interval_refresh_base, 
                            title_button_row, 
                            other_button_row
                    FROM 
      FAQ_settingsbot
                    WHERE id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            settings = cursor.fetchone()
            return settings

    def change_bot_status(self, token, status):
        """Изменить статус бота"""
        query = """ UPDATE 
      FAQ_settingsbot
                    SET status =%s
                    WHERE token =%s """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (status, token))
            self.connection.commit()
