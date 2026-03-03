// Tests for assets/js/i18n.js
// Run with: node --test tests/
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

// Load translations by evaluating i18n.js in a minimal scope
function loadTranslations() {
  const src = readFileSync(join(ROOT, 'assets/js/i18n.js'), 'utf8')
    // Strip the browser-specific runtime code that requires window/document
    .replace(/\/\/ Alusta kieli[\s\S]*$/, '');
  const fn = new Function(src + '; return translations;');
  return fn();
}

// Collect every data-i18n key used across all HTML files
function collectHtmlKeys() {
  const htmlDirs = [ROOT, join(ROOT, 'pages')];
  const keySet = new Set();
  const regex = /data-i18n="([^"]+)"/g;
  for (const dir of htmlDirs) {
    for (const file of readdirSync(dir)) {
      if (!file.endsWith('.html')) continue;
      const content = readFileSync(join(dir, file), 'utf8');
      let match;
      while ((match = regex.exec(content)) !== null) {
        keySet.add(match[1]);
      }
    }
  }
  return keySet;
}

const translations = loadTranslations();
const htmlKeys = collectHtmlKeys();

describe('translations object structure', () => {
  it('has fi, sv and en language sections', () => {
    assert.ok('fi' in translations, 'Missing fi section');
    assert.ok('sv' in translations, 'Missing sv section');
    assert.ok('en' in translations, 'Missing en section');
  });

  it('fi, sv and en sections contain the same set of keys', () => {
    const fiKeys = new Set(Object.keys(translations.fi));
    const svKeys = new Set(Object.keys(translations.sv));
    const enKeys = new Set(Object.keys(translations.en));

    const missingInFi = [...svKeys].filter(k => !fiKeys.has(k));
    const missingInFiFromEn = [...enKeys].filter(k => !fiKeys.has(k));
    const missingInSv = [...fiKeys].filter(k => !svKeys.has(k));
    const missingInSvFromEn = [...enKeys].filter(k => !svKeys.has(k));
    const missingInEnFromFi = [...fiKeys].filter(k => !enKeys.has(k));
    const missingInEnFromSv = [...svKeys].filter(k => !enKeys.has(k));

    assert.deepEqual(missingInFi, [], `Keys in sv but missing in fi: ${missingInFi.join(', ')}`);
    assert.deepEqual(missingInFiFromEn, [], `Keys in en but missing in fi: ${missingInFiFromEn.join(', ')}`);
    assert.deepEqual(missingInSv, [], `Keys in fi but missing in sv: ${missingInSv.join(', ')}`);
    assert.deepEqual(missingInSvFromEn, [], `Keys in en but missing in sv: ${missingInSvFromEn.join(', ')}`);
    assert.deepEqual(missingInEnFromFi, [], `Keys in fi but missing in en: ${missingInEnFromFi.join(', ')}`);
    assert.deepEqual(missingInEnFromSv, [], `Keys in sv but missing in en: ${missingInEnFromSv.join(', ')}`);
  });

  it('no translation value is an empty string', () => {
    for (const lang of ['fi', 'sv', 'en']) {
      for (const [key, value] of Object.entries(translations[lang])) {
        assert.notEqual(value, '', `Empty value for key "${key}" in ${lang}`);
      }
    }
  });
});

describe('HTML translation coverage', () => {
  it('every data-i18n key used in HTML files exists in the fi translation section', () => {
    const missing = [...htmlKeys].filter(k => !(k in translations.fi));
    assert.deepEqual(missing, [], `Keys used in HTML but missing from fi translations: ${missing.join(', ')}`);
  });

  it('every data-i18n key used in HTML files exists in the sv translation section', () => {
    const missing = [...htmlKeys].filter(k => !(k in translations.sv));
    assert.deepEqual(missing, [], `Keys used in HTML but missing from sv translations: ${missing.join(', ')}`);
  });

  it('every data-i18n key used in HTML files exists in the en translation section', () => {
    const missing = [...htmlKeys].filter(k => !(k in translations.en));
    assert.deepEqual(missing, [], `Keys used in HTML but missing from en translations: ${missing.join(', ')}`);
  });
});
