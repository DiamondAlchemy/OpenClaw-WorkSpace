const fs = require('fs');

const files = ['fresh_frozen.json', 'cured.json', 'post_extraction.json'];

files.forEach(file => {
  try {
    const raw = fs.readFileSync(file, 'utf8');
    const data = JSON.parse(raw);
    const rows = data.values;
    
    console.log(`\n=== ${file} ===`);
    if (!rows || rows.length === 0) {
      console.log("No data found.");
      return;
    }

    // Inspect first few rows to identify headers and data start
    for (let i = 0; i < Math.min(5, rows.length); i++) {
      console.log(`Row ${i}:`, JSON.stringify(rows[i]));
    }
  } catch (e) {
    console.error(`Error reading ${file}:`, e.message);
  }
});
