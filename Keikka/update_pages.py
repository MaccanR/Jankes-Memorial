#!/usr/bin/env python3
import os
import re

files = [
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
]

base_path = r"c:\Skola\Jankes\Jankes-Memorial\Keikka"

# CSS block to add
css_block = """    .lang-toggle {
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
"""

toggle_buttons = """      <!-- Language toggle -->
      <div class="absolute top-6 right-6 flex gap-2">
        <button class="lang-toggle active" data-lang="fi" onclick="changeLanguage('fi')">FI</button>
        <button class="lang-toggle" data-lang="sv" onclick="changeLanguage('sv')">SV</button>
      </div>
"""

for file in files:
    full_path = os.path.join(base_path, file)
    
    if os.path.exists(full_path):
        print(f"Updating {file}...")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add i18n.js script if not present
        if '<script src="./i18n.js"></script>' not in content:
            content = content.replace(
                '  </style>',
                '  </style>\n  <script src="./i18n.js"></script>'
            )
        
        # Add lang-toggle CSS if not present
        if '.lang-toggle' not in content:
            content = content.replace(
                '    h1, h2, h3 {\n      font-family: \'Playfair Display\', serif;\n    }',
                f'    h1, h2, h3 {{\n      font-family: \'Playfair Display\', serif;\n    }}\n{css_block}'
            )
        
        # Add language toggle buttons to header if not present
        if 'lang-toggle active' not in content:
            content = re.sub(
                r'(<div class="max-w-5xl mx-auto px-6 py-12 text-center)(">)',
                r'\1 relative\2\n' + toggle_buttons,
                content
            )
        
        # Add data-i18n attributes to labels and values
        translations = {
            "Henkilötiedot": "Henkilötiedot",
            "Sukupuoli:": "Sukupuoli:",
            "Syntynyt:": "Syntynyt:",
            "Kuollut:": "Kuollut:",
            "Hautapaikka:": "Hautapaikka:",
            "Lähisukulaiset": "Lähisukulaiset",
            "Vanhemmat:": "Vanhemmat:",
            "Puoliso:": "Puoliso:",
            "Lapset:": "Lapset:",
            "Sisarukset:": "Sisarukset:",
            "Nainen": "Nainen",
            "Mies": "Mies",
            "Palaa pääsivulle": "Palaa pääsivulle"
        }
        
        for key, value in translations.items():
            # Add data-i18n to dt (labels)
            pattern = rf'(<dt class="font-semibold text-neutral-900">){re.escape(key)}(</dt>)'
            replacement = rf'\1 data-i18n="{key}">{key}\2'
            if f'data-i18n="{key}"' not in content:
                content = re.sub(pattern, replacement, content)
            
            # Add data-i18n to h2 and h3 headings
            for tag in ['h2', 'h3']:
                pattern = rf'(<{tag} class="[^"]*font-semibold[^"]*">){re.escape(key)}(</{tag}>)'
                replacement = rf'\1 data-i18n="{key}">{key}\2'
                if f'data-i18n="{key}"' not in content or f'<{tag}' not in content:
                    content = re.sub(pattern, replacement, content)
            
            # Add data-i18n to dd values for gender
            if key in ["Nainen", "Mies"]:
                pattern = rf'(<dd class="text-neutral-700">){re.escape(key)}(</dd>)'
                replacement = rf'\1 data-i18n="{key}">{key}\2'
                if f'data-i18n="{key}"' not in content:
                    content = re.sub(pattern, replacement, content)
            
            # Add data-i18n to back link
            if key == "Palaa pääsivulle":
                pattern = rf'(<a href="\./index\.html" class="[^"]*">)← {re.escape(key)}(</a>)'
                replacement = rf'\1← <span data-i18n="{key}">{key}</span>\2'
                if f'data-i18n="{key}"' not in content:
                    content = re.sub(pattern, replacement, content)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {file} successfully")
    else:
        print(f"File not found: {full_path}")

print("All files updated!")
