import subprocess


# cmd = "esphome compile testone.yaml" # Здесь вместо date Ваша команда для git
#
#
# returned_output = subprocess.call(cmd) # returned_output содержит вывод в виде строки байтов
# # fddf = returned_output.decode("utf-8")
# #
# # print(type(fddf))
# print('Результат выполнения команды:', returned_output)

def test_xxx(mocker):
    cmd = "esphome compile testone.yaml"
    mocker.spy(subprocess, 'call')
    subprocess.call(cmd)
    assert subprocess.call.call_count == 1