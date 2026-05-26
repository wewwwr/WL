import urllib.request

# Твои исходные списки для DIRECT (белый список)
urls = [
    "https://raw.githubusercontent.com/Master-Yoba/shadowrocket-rules/release/rules-geosite/geosite-ru-mobile-whitelist.list",
    # Ссылка скорректирована на прямой RAW-формат, чтобы скрипт не читал HTML-код страницы
    "https://raw.githubusercontent.com/hxehex/russia-mobile-internet-whitelist/main/whitelist.txt"
]

# Твои ручные домены, которые нужно пустить НАПРЯМУЮ (DIRECT)
combined_rules = {
    "DOMAIN-SUFFIX, yoomoney.ru",
    "DOMAIN-SUFFIX, yoomoney.ru",
    "DEST-PORT,25",
    "DEST-PORT,465",
    "DEST-PORT,587"
}

# СПИСОК ИСКЛЮЧЕНИЙ: впиши сюда домены, которые НЕ НАДО пускать напрямую (удалить из белого списка)
exclusions = {
    "another-domain.ru",
    "another-domain.ru"
}

print("Начинаю загрузку и обработку белых списков...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read().decode('utf-8')
            for line in content.splitlines():
                line = line.strip()
                
                # Игнорируем пустые строки и комментарии
                if not line or line.startswith('#') or line.startswith('//'):
                    continue
                
                # Извлекаем чистый домен для сверки с исключениями
                clean_domain = line.split(',')[-1] if ',' in line else line
                
                # Если домен в исключениях — пропускаем его
                if clean_domain in exclusions:
                    continue
                
                # Приводим к единому стандарту Shadowrocket, если это был просто домен
                if ',' not in line:
                    line = f"DOMAIN-SUFFIX,{line}"
                    
                combined_rules.add(line)
        print(f"Успешно обработан: {url}")
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")

# Сохраняем итоговый белый список
output_filename = "my_custom_direct_list.list"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write("# Auto-generated Shadowrocket Whitelist (DIRECT)\n")
    for rule in sorted(combined_rules):
        f.write(f"{rule}\n")

print(f"Готово! Всего уникальных правил для DIRECT: {len(combined_rules)}")
