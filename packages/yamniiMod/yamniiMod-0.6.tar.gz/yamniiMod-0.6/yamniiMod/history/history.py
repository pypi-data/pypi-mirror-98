import json
class history():
    def __init__(self):
        self.history_arr = None
        """
        """
    def set_history(self, sequence, score):
        #print(score)
        if self.history_arr:
            if self.is_it_dupe_sequence(sequence):
                self.history_arr['dupe'] += 1
                type(self.history_arr['score'])
                if float(score) < float(self.history_arr['score']):
                    #print("menshe")
                    self.history_arr['score'] = float(score)
            else:
                self.history_arr['arrays'].append(sequence)
        else:
            self.history_arr = {'arrays':[sequence],'score': score, 'dupe': 0}
        """
        ▪ принимает 2 переменные
        sequence - массив длинной 500 (int) положительных чисел)
        • score - 1 float
        ▪ проверяет имеющийся массив history_arr на наличие в нем
        дубликата sequence
        ▪ если дубликат найден - проверяет score, и записывает score только
        если оно меньше уже находящегося в данных
        ▪ если дубликат не найден записывает входные данные
        ▪ и ведет счетчик дубликатов
        """
    def is_it_dupe_sequence(self,sequence):
        for i in self.history_arr['arrays']:
            if sequence == i:
                checker = True
                break
            else:
                checker = False
        return checker
        """
        ▪ принимает 1 переменную
        •
        sequence - массив длинной 500 (int) положительных чисел)
        ▪ проверяет, есть ли такая в истории. Если есть True если нет False
        """
    def save_history(self,filepath):
        with open(filepath, "w") as write_file:
            json.dump(self.history_arr, write_file)
        """
        ▪ принимает 1 переменную — filepath
        ▪ записывает данные истории на диск
        """
    def load_history(self,filepath):
        with open(filepath, "r") as read_file:
            self.history_arr = json.load(read_file)

        """
        ▪ принимает 1 переменную — filepath
        ▪ загружает данные истории с диска
        """
