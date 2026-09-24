import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';

const root = resolve('tabtime-extension');
const manifest = JSON.parse(readFileSync(join(root, 'manifest.json'), 'utf8'));
assert.equal(manifest.manifest_version, 3);
assert.equal(manifest.incognito, 'not_allowed');
assert.ok(manifest.content_security_policy.extension_pages.includes("connect-src 'none'"));
const references = [manifest.background.service_worker, manifest.action.default_popup, manifest.options_ui.page, ...Object.values(manifest.icons)];
for (const file of readdirSync(root)) {
  const full = join(root, file);
  if (file.endsWith('.js')) execFileSync(process.execPath, ['--check', full], { stdio: 'pipe' });
  if (file.endsWith('.html')) {
    const html = readFileSync(full, 'utf8');
    for (const match of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
      if (!match[1].startsWith('#')) references.push(match[1]);
    }
  }
  if (/\.(js|html|css)$/.test(file)) {
    const source = readFileSync(full, 'utf8');
    assert.ok(!/\bfetch\s*\(|\bXMLHttpRequest\b|\bWebSocket\s*\(|sendBeacon\s*\(/.test(source), 'Unexpected network API in ' + file);
  }
}
for (const reference of references) assert.ok(existsSync(join(root, reference)), 'Missing local resource: ' + reference);
console.log('Manifest, JavaScript syntax, local resource paths, and absence of network API calls verified.');
