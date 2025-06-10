$bytes = [System.IO.File]::ReadAllBytes("C:\Users\s.papageorgiou\Desktop\Parser Test CAL\translations_reports_NEW.txt")
$enc = [System.Text.Encoding]::GetEncoding(737) # OEM Greek CP737
$content = $enc.GetString($bytes)
[System.IO.File]::WriteAllText("C:\Users\s.papageorgiou\Desktop\Parser Test CAL\translations_reports_NEW_output.txt", $content, [System.Text.Encoding]::UTF8)