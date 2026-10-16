"""Import the preserved Jekyll build into /old without changing the current site.

Usage: python3 import_legacy.py /absolute/path/to/legacy-homepage-664a951-original.zip
Build provenance and the pinned GitHub Pages workflow are in sources/legacy_site.json
and sources/legacy_homepage_build.yml. Archive an existing docs/old before replacing it.
"""
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit, urlunsplit, unquote
import hashlib
import json
import re
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'docs/old'
ORIGIN = 'https://ccipad123.github.io'
BASE = '/old'
AVATAR = BASE + '/images/favicon-portrait.jpg'
TEXT_SUFFIXES = {'.html', '.css', '.js', '.xml', '.json'}
MOBILE_LINK_WRAP = '\n@media(max-width:48em){.archive a,.page__content a{overflow-wrap:anywhere}}\n'


def import_archive(archive):
    if DEST.exists():
        raise SystemExit('docs/old already exists; preserve it in an archive before importing again.')
    changes = []
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        names = {n for n in z.namelist() if not n.endswith('/')}
        assert {'index.html', 'research/index.html', 'awards/index.html', 'links/index.html'} <= names
        for name in names:
            path = PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts, name
        # The original file named 头像.png is JPEG. Preserve its bytes with a matching extension.
        favicon = z.read('images/头像.png')
        assert favicon.startswith(b'\xff\xd8')
        offset = 2
        while offset < len(favicon):
            assert favicon[offset] == 0xff
            marker = favicon[offset + 1]
            length = struct.unpack('>H', favicon[offset + 2:offset + 4])[0]
            if marker in (0xc0, 0xc1, 0xc2):
                height, width = struct.unpack('>HH', favicon[offset + 5:offset + 9])
                break
            offset += 2 + length
        else:
            raise ValueError('JPEG dimensions not found')

        def relocate(url):
            parts = urlsplit(url)
            if parts.netloc and parts.netloc != 'ccipad123.github.io':
                return url
            path = parts.path
            if not path.startswith(BASE + '/') and path != BASE:
                path = BASE + (path if path.startswith('/') else '/' + path)
            rel = unquote(path.removeprefix(BASE + '/'))
            if rel not in names and not path.endswith('/') and rel + '.html' in names:
                path += '.html'
            return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

        for name in sorted(names):
            raw = z.read(name)
            data = raw
            if Path(name).suffix in TEXT_SUFFIXES:
                text = raw.decode('utf-8')
                text = re.sub(r'https?://ccipad123\.github\.io(?![\w.-])(?:/[^\s"\'<>)]*)?',
                              lambda m: relocate(m[0]), text)
                text = re.sub(r'(?P<before>\b(?:href|src|poster|action)\s*=\s*["\'])(?P<url>/(?!/)[^"\']*)(?P<after>["\'])',
                              lambda m: m['before'] + relocate(m['url']) + m['after'], text)
                text = re.sub(r'(?P<before>\burl\(\s*["\']?)(?P<url>/(?!/)[^\s)"\']+)(?P<after>["\']?\s*\))',
                              lambda m: m['before'] + relocate(m['url']) + m['after'], text)
                if name.endswith('.html'):
                    # The original template references favicon sizes absent from its repository.
                    text = re.sub(r'<link\b(?=[^>]*\brel=["\'](?:apple-touch-icon|icon|shortcut icon)["\'])[^>]*>', '', text)
                    text = text.replace('</head>', f'<link rel="icon" type="image/jpeg" href="{AVATAR}"><link rel="apple-touch-icon" href="{AVATAR}"></head>')
                if name == 'images/manifest.json':
                    manifest = json.loads(text)
                    manifest['icons'] = [{'src': AVATAR, 'sizes': f'{width}x{height}', 'type': 'image/jpeg'}]
                    text = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
                if name == 'assets/css/main.css':
                    text += MOBILE_LINK_WRAP
                data = text.encode('utf-8')
            target = DEST / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            if data != raw:
                changes.append(name)
    (DEST / 'images/favicon-portrait.jpg').write_bytes(favicon)
    return {'source_files': len(names), 'changed_text_files': changes,
            'avatar_size': [width, height], 'artifact_sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(import_archive(Path(sys.argv[1]).resolve()), ensure_ascii=False, indent=2))
