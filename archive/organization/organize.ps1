$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..')).TrimEnd('\')
function Safe-Path([string]$relative) {
    $full = [IO.Path]::GetFullPath((Join-Path $projectRoot $relative))
    if (-not $full.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $full" }
    return $full
}
$inventory = @(Import-Csv -LiteralPath (Join-Path $PSScriptRoot 'original-inventory.csv'))
$moves = foreach ($item in $inventory) {
    $path = $item.OriginalPath
    $name = [IO.Path]::GetFileName($path)
    $folder = switch -Regex ($path) {
        '^TabTime_Final_' { 'documents\reports'; break }
        '^IRP \.docx$' { 'documents\research'; break }
        '^test_.*\.docx$' { 'documents\test-documents'; break }
        '^TabTime_Google_Forms_' { 'data\survey-responses'; break }
        '^Google Form in questionnaire|^figures\\fig_gform_questionnaire_' { 'images\screenshots\questionnaire'; break }
        '^form resposses|^figures\\fig_gform_spreadsheet_' { 'images\screenshots\survey-responses'; break }
        '^code screenshots\\|^figures\\fig_code_' { 'images\screenshots\code'; break }
        '^figures\\fig_ui_' { 'images\screenshots\interface'; break }
        '^figures\\fig_gform_overview_mockup' { 'images\mockups'; break }
        '^figures\\fig_gform_' { 'images\charts'; break }
        '^tabtime_google_form_header|^figures\\tabtime_form_banner' { 'images\banners'; break }
        '^figures\\' { 'images\diagrams'; break }
        default { $null }
    }
    $newPath = if ($folder) { Join-Path $folder $name } else { $path }
    [pscustomobject]@{OriginalPath=$path; NewPath=$newPath; SHA256=$item.SHA256; Bytes=$item.Bytes; Status='Unchanged'}
}
foreach ($move in $moves) {
    if ($move.OriginalPath -eq $move.NewPath) { continue }
    $source = Safe-Path $move.OriginalPath
    $destination = Safe-Path $move.NewPath
    if (Test-Path -LiteralPath $destination) { throw "Destination exists: $destination" }
    New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($destination)) -Force | Out-Null
    try {
        Move-Item -LiteralPath $source -Destination $destination
        $move.Status = 'Moved'
    } catch {
        $move.NewPath = $move.OriginalPath
        $move.Status = 'Left in place: ' + $_.Exception.Message
    }
    $moves | Export-Csv -LiteralPath (Join-Path $PSScriptRoot 'file-moves.csv') -NoTypeInformation
}
foreach ($directory in @('extracted_irp','extracted_tabtime','code screenshots','figures','tabtime extentions')) {
    $source = Safe-Path $directory
    $category = if ($directory.StartsWith('extracted_')) { 'extracted-documents' } else { 'unused-folders' }
    if ($category -eq 'unused-folders' -and @(Get-ChildItem -LiteralPath $source -Force -Recurse -File).Count -gt 0) { continue }
    $relativeDestination = 'archive\' + $category + '\' + $directory
    $destination = Safe-Path $relativeDestination
    if (Test-Path -LiteralPath $destination) { throw "Destination exists: $destination" }
    New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($destination)) -Force | Out-Null
    Move-Item -LiteralPath $source -Destination $destination
    foreach ($move in $moves) {
        if ($move.NewPath.StartsWith($directory + '\')) {
            $move.NewPath = $relativeDestination + $move.NewPath.Substring($directory.Length)
            $move.Status = 'Moved'
        }
    }
    $moves | Export-Csv -LiteralPath (Join-Path $PSScriptRoot 'file-moves.csv') -NoTypeInformation
}
foreach ($move in $moves) {
    $destination = Safe-Path $move.NewPath
    if (-not (Test-Path -LiteralPath $destination -PathType Leaf)) { throw "Missing: $destination" }
    if ($move.SHA256 -and (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $move.SHA256) { throw "Content changed: $destination" }
}
$duplicates = @($moves | Where-Object SHA256 | Group-Object SHA256 | Where-Object Count -gt 1 | ForEach-Object {
    [pscustomobject]@{SHA256=$_.Name; Files=@($_.Group.NewPath)}
})
ConvertTo-Json -InputObject $duplicates -Depth 4 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'duplicate-files.json')
[pscustomobject]@{OriginalFiles=$moves.Count; Moved=@($moves | Where-Object Status -eq 'Moved').Count; VerifiedByHash=@($moves | Where-Object SHA256).Count; DuplicateGroups=$duplicates.Count; Exceptions=@($moves | Where-Object Status -like 'Left in place*')} | ConvertTo-Json -Depth 4
