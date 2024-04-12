from datetime import datetime, timedelta

def converter_horario(horario_utc3):
    # Subtrai 3 horas do horário UTC
    horario_local = horario_utc3 - timedelta(hours=3)
    
    # Formata a hora como 'HH:MM'
    hora_formatada = horario_local.strftime('%H:%M')
    
    # Formata o dia como 'YYYY-MM-DD'
    dia_formatado = horario_local.strftime('%d/%m/%Y')
    
    return {'hora': hora_formatada, 'dia' : dia_formatado}