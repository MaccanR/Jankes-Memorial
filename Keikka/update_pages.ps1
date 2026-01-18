# PowerShell script to update person pages with i18n system
$files = @(
  "ahlgren-amanda-fredrika.html",
  "ahlgren-georg-fredrik.html",
  "jankes-arthur.html",
  "jankes-bros-fredrik.html",
  "jankes-carl-emil.html",
  "jankes-georg-fredrik.html",
  "jankes-hjordis-irene.html",
  "jankes-karl-emil.html",
  "jankes-sigrid-maria.html",
  "jankes-sofia.html",
  "jankes-sven-olof-aarmand.html",
  "lindh-fredrik-mikael.html",
  "lindh-irma-annikki.html",
  "luukkonen-ulla-kristiina.html",
  "roos-elsa-irene.html",
  "roos-ulla-maria.html",
  "sidorow-emilia-vilhelmina.html",
  "silander-elsa-maria.html",
  "silander-maria-georgina.html",
  "silander-signe-maria.html"
)

$basePath = "c:\Skola\Jankes\Jankes-Memorial\Keikka"

foreach ($file in $files) {
  $fullPath = Join-Path $basePath $file
  
  if (Test-Path $fullPath) {
    Write-Host "Updating $file..."
    $content = Get-Content $fullPath -Raw
    
    # Add i18n.js script reference if not present
    if ($content -notmatch '<script src="\./i18n\.js"></script>') {
      $content = $content -replace '(</style>)', '</style>' + "`n" + '  <script src="./i18n.js"></script>'
    }
    
    # Add lang-toggle CSS if not present
    if ($content -notmatch '\.lang-toggle') {
      $cssBlock = @"
    .lang-toggle {
      cursor: pointer;
      padding: 0.5rem 1rem;
      background-color: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.3);
      border-radius: 0.375rem;
      font-size: 0.875rem;
      transition: all 0.3s ease;
    }
    .lang-toggle:hover {
      background-color: rgba(255,255,255,0.2);
      border-color: rgba(255,255,255,0.5);
    }
    .lang-toggle.active {
      background-color: rgba(255,255,255,0.3);
      border-color: rgba(255,255,255,0.6);
      font-weight: 600;
    }
"@
      $content = $content -replace "(h1, h2, h3 \{[\s\S]*?\})", ('$1' + "`n" + $cssBlock)
    }
    
    # Add language toggle buttons to header if not present
    if ($content -notmatch 'lang-toggle active') {
      $toggleButtons = @"
      <!-- Language toggle -->
      <div class="absolute top-6 right-6 flex gap-2">
        <button class="lang-toggle active" data-lang="fi" onclick="changeLanguage('fi')">FI</button>
        <button class="lang-toggle" data-lang="sv" onclick="changeLanguage('sv')">SV</button>
      </div>
"@
      $content = $content -replace '(<div class="max-w-5xl mx-auto px-6 py-12 text-center)', ('$1 relative' -replace 'text-center', 'text-center relative')
      $content = $content -replace '(<div class="max-w-5xl mx-auto px-6 py-12 text-center relative">)', ('$1' + "`n" + $toggleButtons)
    }
    
    # Add data-i18n attributes to labels
    $translations = @{
      "Henkilötiedot" = "Henkilötiedot"
      "Sukupuoli:" = "Sukupuoli:"
      "Syntynyt:" = "Syntynyt:"
      "Kuollut:" = "Kuollut:"
      "Hautapaikka:" = "Hautapaikka:"
      "Lähisukulaiset" = "Lähisukulaiset"
      "Vanhemmat:" = "Vanhemmat:"
      "Puoliso:" = "Puoliso:"
      "Lapset:" = "Lapset:"
      "Sisarukset:" = "Sisarukset:"
      "Nainen" = "Nainen"
      "Mies" = "Mies"
      "Palaa pääsivulle" = "Palaa pääsivulle"
    }
    
    foreach ($key in $translations.Keys) {
      # Add data-i18n to dt (labels)
      $content = $content -replace "(<dt class=""font-semibold text-neutral-900"">$([regex]::Escape($key))</dt>)", ('<dt class="font-semibold text-neutral-900" data-i18n="' + $key + '">' + $key + '</dt>')
      
      # Add data-i18n to dd (values) for gender and back link
      if ($key -in @("Nainen", "Mies", "Palaa pääsivulle")) {
        $content = $content -replace "(<(?:dd|a)[^>]*>$([regex]::Escape($key))</(?:dd|a)>)", ('<$1 data-i18n="' + $key + '">' + $key + '</$2>')
      }
      
      # Add data-i18n to headings
      if ($key -in @("Henkilötiedot", "Lähisukulaiset")) {
        $content = $content -replace "(<(?:h2|h3)[^>]*>$([regex]::Escape($key))</(?:h2|h3)>)", ('<$1 data-i18n="' + $key + '">' + $key + '</$2>')
      }
    }
    
    Set-Content $fullPath $content
    Write-Host "Updated $file successfully"
  } else {
    Write-Host "File not found: $fullPath"
  }
}

Write-Host "All files updated!"
