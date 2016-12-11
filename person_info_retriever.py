import requests
from bs4 import BeautifulSoup

from string import Template


class PersonInfoRetriever(object):
    def __init__(self):
        with open('message_templates/answer_template.txt') as fin:
            self.answer_template = Template(fin.read())

    @staticmethod
    def parse_table_line(table_line):
        td_tags_texts = list(map(lambda x: x.text, table_line.find_all('td')[2:]))
        person_info = {
            'full_name': td_tags_texts[0],
            'seminarian_surname': td_tags_texts[1],
            'test_1': td_tags_texts[2],
            'test_2': td_tags_texts[3],
            'test_3': td_tags_texts[4],
            'test_4': td_tags_texts[5],
            'test_5': td_tags_texts[6],
            'essay': td_tags_texts[10],
            'project': td_tags_texts[11],
            'rating': td_tags_texts[13],
            'auto_exam_pass': td_tags_texts[15]
        }

        return person_info

    @staticmethod
    def find_person_info_by_full_name(full_name):
        rating_url = 'https://docs.google.com/spreadsheets/u/1/d/19w5v_GkkijkoJnpQTHrok6hWc_ZWaofKzjfPZorKeGU/pubhtml?gid=2100108390&single=true'
        r = requests.get(rating_url)  # TODO: check return value
        soup = BeautifulSoup(r.text, 'html.parser')

        tr_tags = soup.find_all('tr', {'style': 'height:19px;'})[2:]
        info = {
            'n_students': len(tr_tags),
            'n_students_with_auto_exam_pass': len(tr_tags) // 3
        }

        n_students_with_auto_exam_pass_before = 0

        for position, table_line in enumerate(tr_tags):
            info.update(PersonInfoRetriever.parse_table_line(table_line))
            info['position'] = position + 1

            if info['full_name'].startswith(full_name):
                info['n_students_with_auto_exam_pass_before'] = n_students_with_auto_exam_pass_before
                return info

            print(info['auto_exam_pass'])
            if info['auto_exam_pass'] == 'ИСТИНА':
                n_students_with_auto_exam_pass_before += 1

        return None

    def format_person_info(self, person_info):
        return self.answer_template.substitute(person_info)

    def get_person_info_by_full_name(self, full_name):
        person_info = PersonInfoRetriever.find_person_info_by_full_name(full_name)
        if person_info is not None:
            return self.format_person_info(person_info)
        else:
            return 'Не смог ничего найти :( Возможно вы ошиблись в ФИО?\n'

if __name__ == '__main__':
    person_info_retriever = PersonInfoRetriever()
    print(person_info_retriever.get_person_info_by_full_name('Искаков'))