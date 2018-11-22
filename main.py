from power_edit import power_edit

power_edit = power_edit.PowerEdit()
results = power_edit.find_files('C:\\Users\\gbmhu\\code\\Hugo\\quickstart\\content\\' + '**/*.md', recursive=True)
print(results[0])

power_edit.find_replace(results[0], '\[caption.*\[/caption\]', 'test', regex=True)