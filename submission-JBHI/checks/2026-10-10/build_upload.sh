#!/bin/zsh
# Fill submission-JBHI/upload from the verified cleaned copy: source/, two PDFs and a source zip.
set -e
cd "${0:A:h}/../.."
R=checks/2026-10-10
rm -rf upload; mkdir -p upload/source
cp -R $R/upload_clean/. upload/source/
B=$(mktemp -d); cp -R upload/source/. $B/; rm -f $B/*.pdf
(cd $B && pdflatex -interaction=nonstopmode main.tex >/dev/null && pdflatex -interaction=nonstopmode main.tex >/dev/null && pdflatex -interaction=nonstopmode supplement.tex >/dev/null && pdflatex -interaction=nonstopmode supplement.tex >/dev/null)
cp $B/main.pdf upload/Manuscript.pdf; cp $B/supplement.pdf upload/Supplementary_Material.pdf
cp $B/main.pdf upload/source/main.pdf; cp $B/supplement.pdf upload/source/supplement.pdf
(cd upload/source && zip -q -r -X ../LaTeX_source.zip . -x '.*')
echo "pages: $(pdfinfo upload/Manuscript.pdf | grep Pages) + $(pdfinfo upload/Supplementary_Material.pdf | grep Pages)"
echo "undefined refs: $(grep -c -i undefined $B/main.log) / $(grep -c -i undefined $B/supplement.log)"
diff <(pdftotext ../drafts/manuscriptv2/main.pdf - ) <(pdftotext upload/Manuscript.pdf -) >/dev/null && echo "Manuscript.pdf text = v2 main.pdf" || echo "Manuscript.pdf text DIFFERS from v2"
diff <(pdftotext ../drafts/manuscriptv2/supplement.pdf - ) <(pdftotext upload/Supplementary_Material.pdf -) >/dev/null && echo "Supplementary text = v2" || echo "Supplementary DIFFERS from v2"
pdfinfo upload/Manuscript.pdf | grep -E "^(Title|Author|Subject|Keywords|Creator|Producer)"
