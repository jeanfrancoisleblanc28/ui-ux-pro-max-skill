# CV — Jean-François Leblanc, CPA

CV deux pages (A4) pour le poste de commissaire industriel.

- `cv-jean-francois-leblanc.html` — source autonome (polices Cormorant Garamond + Inter embarquées en base64, aucune dépendance réseau). S'ouvre dans un navigateur; l'impression (Ctrl+P, marges « aucune », format A4) reproduit exactement le PDF.
- `cv-jean-francois-leblanc.pdf` — export prêt à envoyer, généré depuis le HTML avec Chromium headless :

```bash
chromium --headless --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=cv-jean-francois-leblanc.pdf cv-jean-francois-leblanc.html
```

Champ restant à compléter avant envoi : `[Ville]` (bureau Deloitte).
