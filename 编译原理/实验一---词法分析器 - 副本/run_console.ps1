# PowerShell版本的控制台词法分析器运行脚本

Write-Host "正在编译控制台版本词法分析器..."
$compileResult = cmd /c "cl /EHsc main_simple.cpp lexer.cpp /Fe""词法分析器_simple.exe"" /link 2>&1"
Write-Host $compileResult

if ($LASTEXITCODE -ne 0) {
    Write-Host "编译失败！"
    Start-Sleep -Seconds 5
    exit 1
}

Write-Host "编译成功！"

Write-Host ""
Write-Host "请选择要分析的测试文件："
Write-Host "1. program1.txt"
Write-Host "2. program2.txt"
Write-Host "3. program3.txt"
Write-Host ""

do {
    $choice = Read-Host "请输入选项 (1-3)"
} until ($choice -ge 1 -and $choice -le 3)

switch ($choice) {
    1 { $inputFile = "program1.txt" }
    2 { $inputFile = "program2.txt" }
    3 { $inputFile = "program3.txt" }
}

Write-Host ""
Write-Host "运行词法分析器..."
Write-Host "分析文件: $inputFile"
Write-Host ""

Start-Process -FilePath ".\词法分析器_simple.exe" -ArgumentList $inputFile -NoNewWindow -Wait

Write-Host ""
Write-Host "程序执行完毕，按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")