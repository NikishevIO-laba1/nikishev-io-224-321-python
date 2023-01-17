# py-файл:
# - Через параметры командной строки получить путь к анализируемой папке и другие параметры (например, исключения, вложенность, типы файлов и т.п.), в том числе путь к БД (если не задан путь, то предусмотреть путь по умолчанию, например, рядом с анализируемой папкой).
# - Рекурсивно пройтись по полученному пути, найти все необходимые файлы и обработать их, а в консоль выводить этапы выполнения и/или прогресс выполнения, предусмотреть возможность отмены и/или паузы.
# - По каждому файлу достать всю информацию (атрибуты, метаданные, tags и т.п.), в том числе и превью файла (например, 15 секунд) и сохранить это в БД.
# - Если БД для хранения информации о файлах не создана, то ее необходимо создать и начать заполнение данными.
# - Если БД создана и там уже хранится какая-то информация о файле, то предусмотреть возможность ее обновления или пропуска, например, управлять этим через командную строку.
# - Через параметры командной строки добавить механизм экспортирования некоторых данных в CSV-файл.

# ipynb-файл:
# - Создать несколько типичных запросов к БД, на которых можно было бы увидеть основные возможности выборки данных, желательно с использованием NumPy, Pandas, Matplotlib и т.п. (минимум 10 выборок).
# Например:
# - показать ТОП самых больших файлов в байтах, по ширине, по высоте и т.п.;
# - показать ТОП самых новых файлов по дате создания, по дате съемки и т.п.;
# - построить график по размеру файлов, по типам файлов и т.п.

# Уточнение:
# - БД создаем на SQLite, проектируем ее самостоятельно.
# - Предусмотреть возможность работы с различными типами файлов.
# - Предусмотреть возможность обновления данных в БД. 
# - Предусмотреть обработку потенциальных ошибок.
# - Для демонстрации возможностей использовать разные типы файлов, множество подкаталогов, различные параметры, возможные ошибки и т.п.
# - Помним, что, например, в файлах mp3 есть различные версии тегов, в которых находятся данные: название альбома, фото, исполнитель, жанр и т.п.

import warnings
def insert_flatten(cur, nodicts, dicts, filename, path):
    """вставляет словарь в базу данных, nodicts - словарь без вложенных словарей, dicts - с"""
    #cur.execute(f"""INSERT INTO "audiofiles"("{'","'.join(nodicts.keys())}") VALUES("{'","'.join(nodicts.values())}")""")
    #print(f"""INSERT INTO "audiofiles" ("{'","'.join(nodicts.keys())}") VALUES({'?, '*(len(nodicts.keys())-1)}?)""")
    cur.execute(f"""INSERT INTO "audiofiles" ("{'","'.join(nodicts.keys())}") VALUES({'?, '*(len(nodicts.keys())-1)}?)""", tuple(nodicts.values()))
    for key,value in dicts.items():
    #if key=='filename': key='path'
        if type(value)==dict: 
            for key1,value1 in value.items():
                value1=''.join(list(i for i in value1 if i.isalnum()))
                #print(f'UPDATE "audiofiles" SET "{key+"_"+key1}" = "{value1}" WHERE "filename" = "{filename}"')
                cur.execute(f'UPDATE "audiofiles" SET "{key+"_"+key1}" = "{value1}" WHERE "filename" = "{filename}"')
    audio=open_audio(path)
    #print(f'UPDATE "audiofiles" SET "preview" = ? WHERE "filename" = "{filename}"')
    cur.execute(f'UPDATE "audiofiles" SET "preview" = ? WHERE "filename" = "{filename}"', ((audio,) if audio is not None else (0,)))

def update_flatten(cur, data, filename, path):
    """обновляет базу данных словарём"""
    for key,value in data.items():
        #if key=='filename': key='path'
        if type(value)==dict: 
            for key1,value1 in value.items():
                value1=''.join(list(i for i in value1 if i.isalnum()))
                #print(f'UPDATE "audiofiles" SET "{key+"_"+key1}" = "{value1}" WHERE "filename" = "{filename}"')
                cur.execute(f'UPDATE "audiofiles" SET "{key+"_"+key1}" = "{value1}" WHERE "filename" = "{filename}"')
        #print(f'UPDATE "audiofiles" SET "{key}" = "{value}" WHERE "filename" = "{filename}"')
        else:cur.execute(f'UPDATE "audiofiles" SET "{key}" = "{value}" WHERE "filename" = "{filename}"')
    audio=open_audio(path)
    cur.execute(f'UPDATE "audiofiles" SET "preview" = ? WHERE "filename" = "{filename}"', ((audio,) if audio is not None else (0,)))

import numpy
def open_audio(filename=None, lib='auto',duration_seconds=5, log=False, blob=True):
    """возвращяет первые x секунд"""
    if lib=='auto' and log is True: print('создаётся превью для', filename)
    n=0
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if lib=='pedalboard.io':
            from pedalboard.io import AudioFile
            
            with AudioFile(filename).resampled_to(44100) as f:
                audio = f.read(f.frames)
                samplerate = 44100
                duration=duration_seconds*samplerate
                if len(audio)>duration or len(audio[0])>duration: return audio,samplerate
                elif len(audio)>16: audio=audio[:duration]
                else: 
                    for i in range(len(audio)): audio[i]=audio[i,:duration]
            audio=audio.T
        elif lib=='librosa':
            import librosa
            audio, samplerate = librosa.load(filename, sr=44100, duration=duration_seconds, mono=False)
            audio=audio.T
        elif lib=='soundfile':
            import soundfile
            audio, samplerate = soundfile.read(filename, always_2d=True)
            #audio=audio.T
            if len(audio[0])<duration_seconds*samplerate: 
                for i in range(len(audio)): audio[i]=audio[i,:duration_seconds*samplerate]
        elif lib=='madmom':
            import madmom
            audio, samplerate = madmom.io.audio.load_audio_file(filename, dtype=float, stop=duration_seconds)
            #audio=audio.T
        # elif lib=='pydub':
        #     from pydub import AudioSegment
        #     song=AudioSegment.from_file(filename)
        #     audio = song.get_array_of_samples()
        #     samplerate=song.frame_rate
        #     print(audio)
        #     print(filename)
        elif lib=='auto':
            for i in ('madmom', 'librosa','soundfile', 'pedalboard.io'):
                #print(i)
                try: 
                    return open_audio(filename, i, blob=blob)
                except:
                    #print(e)
                    n+=1
    #print(n)
    if n==4: 
        print('не удалось создать превью для '+ filename+', не аудио файл?')
        return None
    if log is True: print('сохраняется')
    if blob is True:
        import soundfile
        soundfile.write('temp/temp.mp3', audio, samplerate)
        with open('temp/temp.mp3', 'rb') as f: blob=f.read()
        return blob
    else: 
        return audio,samplerate

folder=None
print('Начинаем')
depth=0
exclude={}
filetypes={'mp3', 'wav', 'flac', 'ogg', 'aac', 'wma', 'm3a', 'aif'}
mode='skip'
csv,csv_columns,show,play=None,None,None,None
output='Никишев.db'

try:
    import sys,getopt
    args, idk = getopt.getopt(sys.argv[1:],"f:e:d:t:o:m:c:l:a:b:",["folder=","exclude=",'depth=','filetypes=','output=', 'mode=','csv=','columns=','show=','play='])
    for i in args:
        #print(i)
        if i[0]=='-f' or i[0]=='--folder': 
            folder=i[1].replace('\\','/').replace('"','').replace("'",'')
            initial_depth=folder.count('/')
        if i[0]=='-e' or i[0]=='--exclude': exclude={i.replace('\\','/').replace('"','').replace("'",'') for i in i[1].split('?')}
        if i[0]=='-d' or i[0]=='--depth': depth=int(i[1].replace('"','').replace("'",''))
        if i[0]=='-t' or i[0]=='--filetypes': filetypes={i.lower().replace('"','').replace("'",'') for i in i[1]}
        if i[0]=='-o' or i[0]=='--output': output=i[1].replace('"','').replace("'",'')
        if i[0]=='-m' or i[0]=='--mode': mode=i[1].replace('"','').replace("'",'')
        if i[0]=='-c' or i[0]=='--csv': csv=i[1].replace('\\','/').replace('"','')
        if i[0]=='-l' or i[0]=='--columns': csv_columns=i[1].replace(' ','').replace("'",'').split(',')
        if i[0]=='-a' or i[0]=='--show': show=i[1].replace('"','')
        if i[0]=='-b' or i[0]=='--play': play=i[1].replace("'",'').replace("'",'')
        #print(csv_columns)
except Exception as e: print(e)

#folder=r'F:\Stuff\Producing\Projects\Unreleased\Lifetime'
import tqdm
print('Подключаемся к базе данных')
import sqlite3,os
try:
    with sqlite3.connect(output) as con:
        con.row_factory = lambda cursor, row: row[1] if len(row)>1 else row[0]
        cur=con.cursor()
        if cur.execute("SELECT name FROM sqlite_master WHERE name='audiofiles'").fetchone() is None: cur.execute("CREATE TABLE audiofiles(filename TEXT, preview BLOB, path TEXT, PRIMARY KEY(path ASC))")
        if folder is not None:
            print('Смотрим файлы')
            from pydub.utils import mediainfo
            import time
            #print(folder)
            #print(os.listdir(folder))
            for r, d, f in tqdm.tqdm(os.walk(folder, topdown=True)):
                #print(r)
                #print (r, r.count('/') + r.count('\\'), initial_depth+depth, r.count('/') + r.count('\\') > initial_depth+depth)
                if depth>0 and r.count('/') + r.count('\\') > initial_depth+depth: continue#глубина
                d_absolute={r+'/'+i for i in d}
                f_absolute={r+'/'+i for i in f}
                #print(exclude)
                for i in exclude:#исключения
                    #print(i in d_absolute)
                    #print(i, d_absolute)
                    if i in d_absolute: d.remove(i.split('/')[-1])
                for f in f_absolute:
                    #print(f)
                    if f.lower().split('.')[-1] in filetypes:
                        filename=f.split('/')[-1]
                        data=mediainfo(f)
                        if 'filename' not in data: data['filename']=f
                        if 'format_name' not in data: data['format_name']=filename.split('.')[-1]
                        fileinfo=os.stat(f)
                        n=0
                        for i in ('st_mode', 'st_ino', 'st_dev', 'st_nlink', 'st_uid', 'st_gid', 'st_size', 'st_atime', 'st_mtime', 'st_ctime'):
                            if i in data.keys(): continue
                            if i=='st_size': 
                                data['size']=fileinfo[n]
                                continue
                            data[i]=fileinfo[n]
                            if 'time' in i: data[i+'_formatted']=time.ctime(fileinfo[n])
                            n+=1
                        data['path'] = data.pop('filename').replace('\\','/')
                        data['filename']=filename
                        #print(data)
                        #input()
                        #columns=list(i[1] for i in (cur.execute('PRAGMA table_info(audiofiles);').fetchall()))
                        columns=cur.execute('PRAGMA table_info(audiofiles);').fetchall()
                        data2=data.copy()
                        for key,value in data.copy().items():
                            #if key=='filename': key='path'
                            if type(value)==int: variable='INTEGER'
                            elif type(value)==float: variable='REAL'
                            elif type(value)==str and value.isdigit(): variable='INTEGER'
                            elif type(value)==str and value.replace('.','',1).isdigit(): variable='REAL'
                            elif type(value)==str: variable='TEXT'
                            else: variable='BLOB'
                            if type(value)!=dict and key.casefold() not in (c.casefold() for c in columns):
                                #print(f'ALTER TABLE "audiofiles" ADD COLUMN "{key}" {variable}')
                                cur.execute(f'ALTER TABLE "audiofiles" ADD COLUMN "{key}" {variable}')
                                #con.commit()
                            if type(value)==dict:
                                for key1,value1 in value.items():
                                    if type(value1)==int: variable='INTEGER'
                                    elif type(value1)==float: variable='REAL'
                                    elif type(value1)==str and value1.isdigit(): variable='INTEGER'
                                    elif type(value1)==str and value1.replace('.','',1).isdigit(): variable='REAL'
                                    elif type(value1)==str: variable='TEXT'
                                    else: variable='BLOB'
                                    if variable=='TEXT': value1=''.join(list(c for c in value1 if c.isalnum()))
                                    if (key+'_'+key1).casefold() not in (c.casefold() for c in columns):
                                        #print(key+'_'+key1, columns)
                                        cur.execute(f'''ALTER TABLE "audiofiles" ADD COLUMN "{key+'_'+key1}" "TEXT"''')
                                data2.pop(key)
                        filenames=cur.execute('SELECT "filename" FROM "audiofiles"').fetchall()
                        #print(mode.lower())
                        #print(mode.lower()=='skip' or mode.lower()=='s')
                        if mode.lower()=='skip' or mode.lower()=='s':
                            #print(filenames)
                            if filename in filenames: continue
                            #print(filename)
                            insert_flatten(cur, data2, data, filename, f)
                        elif mode.lower()=='update' or mode.lower()=='u':
                            if filename in filenames:update_flatten(cur, data, filename, f)
                            else:insert_flatten(cur, data2, data, filename, f)
                        else:
                            if filename in filenames: update_flatten(cur, data, filename, f) if input(f'{filename} уже есть в базе данных. Перезаписать? (y/n): ').lower()==('y') else False
            print('Записываем изменения в базу данных.')
            con.commit()
            print('Операция завершена.')

        def audio2numpy(bytes):
            """функция чтобы получить аудио"""
            with open('temp/temp.mp3', 'wb')as f:
                f.write(bytes)
            return open_audio('temp/temp.mp3', lib='auto',duration_seconds=5, log=False, blob=False)

        def play_audio(filename):
            """Функция чтобы проиграть превью файла по его имени"""
            print('Проигрывается превью',filename)
            with open('temp/temp.mp3', 'wb')as f:
                data = cur.execute(f'SELECT "preview" FROM "audiofiles" WHERE "filename" = "{filename}"').fetchall()[0]
                if data is None: 
                    print (f'Файл {filename} не содержит аудио данных.')
                    return
                else: f.write(data)
            import vlc
            sound = vlc.MediaPlayer()
            media=vlc.Media('temp/temp.mp3')
            sound.set_media(media)
            sound.play()
            import time
            time.sleep(min(5, float(cur.execute(f'SELECT "duration" FROM "audiofiles" WHERE "filename" = "{filename}"').fetchall()[0])))
        
        if play is not None:
            play_audio(play)
        #play('nikishev. - Lifetime.mp3')

        #csv='csv.csv'
        #csv_columns=['filename', 'path', 'duration']
        #print(csv_columns)
        #input(cur.execute('PRAGMA table_info(audiofiles);').fetchall())
        import pandas
        con.row_factory=None
        if csv is not None and csv_columns is not None:
            print('Записывается .csv файл '+csv)
            #print(f'''SELECT {','.join(csv_columns)} FROM audiofiles''')
            #print(cur.execute(f'''SELECT {','.join(csv_columns)} FROM audiofiles''').fetchall())
            pd=pandas.read_sql(f'''SELECT {','.join(csv_columns)} FROM audiofiles''', con)
            pd.to_csv(csv, index=False)

        cur.row_factory=None
        #show='SELECT TAG_date, size FROM audiofiles'
        def get(query, show=False):
            global cur
            cur.row_factory=None
            if show is True:
                cur.execute(query)
                from prettytable import PrettyTable,from_db_cursor
                table = from_db_cursor(cur)
                print(table)
            return cur.execute(query).fetchall()

        if show is not None:get(show, True)
        # def close(): 
        #     global con
        #     con.close()
        # if __name__ == '__main__':
        #     con.close()

except KeyboardInterrupt:
    con.close()
    print('Операция завершена пользователем.')
# except Exception as e:
#     con.close()
#     print(e)
