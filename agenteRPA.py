import pyautogui
import time 
import os
from google import genai
import pyperclip  
# pip install google-genai
# pip install pyperclip
cliente = genai.Client()
response = cliente.models.generate_content(
    model='gemini-3.6-flash',
    contents='Me explique em 3 linhas o que é calor'
)

# $env:GEMINI_API_KEY="chavedaapi" /dentro do terminal

print(response.text)
pyautogui.FAILSAFE= True
print("ROBÔ TRABALHANDO PARA VOCÊ...")
time.sleep(1)
pyautogui.press('win')
time.sleep(1)
pyautogui.write('notepad',interval=0.005)
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.hotkey('ctrl','a')
time.sleep(1)
pyautogui.press('delete')
# texto = '''---RELATORIO DE CADASTRO
# Cliente: Marcos da Silva
# Status: Aprovado
# Processo concluído com sucesso.
# '''
pyperclip.copy(response.text)
pyautogui.hotkey('ctrl', 'v')
# pyautogui.write(response.text, interval=0.05)
time.sleep(1)
print('Salvando Arquivo')
pyautogui.hotkey('ctrl','s')
pyautogui.write(' relatorio.txt',interval=0.005)
pyautogui.press('enter')
time.sleep(1)
pyautogui.press('left')
pyautogui.press('enter')
print('Relatório salvo com sucesso.')
