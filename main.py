from power_edit import power_edit

num_replacements = 0

def strict_find(string, find, start_pos):
    index = string.find(find, start_pos)
    if index == -1:
        raise RuntimeError(f'The text {find} was not found in {string}.')
    return index

def replace_fn_caption_tag(find_str: str) -> str:
    # print(f'find_str = {find_str}')

    # WIDTH
    width_start_index = strict_find(find_str, 'width="', 0) + 7
    width_stop_index = strict_find(find_str, '"', width_start_index)
    # print(width_start_index)
    # print(width_stop_index)
    width = find_str[width_start_index:width_stop_index]
    # print(f'width = {width}')

    # URL begins after first (
    url_start_index = strict_find(find_str, '(', 0) + 1
    # print(url_start_index)
    url_stop_index = strict_find(find_str, ')', url_start_index)
    url = find_str[url_start_index:url_stop_index]
    # print(f'url = {url}')

    # Caption begins after first ) after url_stop_index
    # Caption ends before next ]
    caption_start_index = strict_find(find_str, ')', url_stop_index + 1) + 2
    # print(f'caption_start_index = {caption_start_index}')
    
    caption_stop_index = strict_find(find_str, '[', caption_start_index)
    # print(f'caption_stop_index = {caption_stop_index}')

    caption = find_str[caption_start_index:caption_stop_index]
    # print(f'caption = {caption}')

    # Substitue values into template
    template = '{{< figure src="<URL>" width="<WIDTH>" caption="<CAPTION>" caption-position="bottom" >}}'
    template = template.replace('<URL>', url)
    template = template.replace('<WIDTH>', width)
    template = template.replace('<CAPTION>', caption)
    # print(f'replaced_str = {template}')

    global num_replacements
    num_replacements = num_replacements + 1

    return template

def replace_fn_no_caption_tag(find_str: str) -> str:
    print(find_str)
    return ''

power_edit = power_edit.PowerEdit()
results = power_edit.find_files('/Users/ghunter/code/HugoTest/content/' + '**/*.md', recursive=True)
# print(results[0])

for i in range(1):
    print(f'Processing file {results[i]}')
    # power_edit.find_replace_regex(results[i], '\[caption.*?\[/caption\]', replace_fn_caption_tag, multiline=True)

    pattern = '\[\!\[.*?\]\(.*?\)\]\(.*?\)'
    pattern = '\[\!\[.*?\]\(.*?\).*?\]\(.*?\)'
    power_edit.find_replace_regex(results[i], pattern, replace_fn_no_caption_tag, multiline=True)

print(f'num_replacements = {num_replacements}')