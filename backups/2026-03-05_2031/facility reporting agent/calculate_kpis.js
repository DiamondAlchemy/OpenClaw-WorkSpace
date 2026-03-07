const fs = require('fs');

const TARGET_MONTH = 1; // February is 1 (0-indexed)
const TARGET_YEAR = 2026;

// Helper to parse date "M/D/YYYY"
function parseDate(dateStr) {
  if (!dateStr) return null;
  const parts = dateStr.trim().split('/');
  if (parts.length !== 3) return null;
  return new Date(parts[2], parts[0] - 1, parts[1]);
}

// Helper to check if date is in target month/year
function isTargetPeriod(dateStr) {
  const d = parseDate(dateStr);
  if (!d) return false;
  return d.getMonth() === TARGET_MONTH && d.getFullYear() === TARGET_YEAR;
}

// Load data
const ffData = JSON.parse(fs.readFileSync('fresh_frozen.json', 'utf8')).values;
const curedData = JSON.parse(fs.readFileSync('cured.json', 'utf8')).values;
const postData = JSON.parse(fs.readFileSync('post_extraction.json', 'utf8')).values;

// Process Extraction Runs (Fresh Frozen & Cured)
// FF & Cured data starts at index 2
const ffRows = ffData.slice(2).filter(row => row && row[2] && isTargetPeriod(row[2]));
const curedRows = curedData.slice(2).filter(row => row && row[2] && isTargetPeriod(row[2]));

const totalFFRuns = ffRows.length;
const totalCuredRuns = curedRows.length;
const totalExtractionRuns = totalFFRuns + totalCuredRuns;

// Total Biomass (lbs)
// Index 1: Weight Received (Lbs)
const ffBiomass = ffRows.reduce((sum, row) => sum + (parseFloat(row[1]) || 0), 0);
const curedBiomass = curedRows.reduce((sum, row) => sum + (parseFloat(row[1]) || 0), 0);
const totalBiomassLbs = ffBiomass + curedBiomass;

// Process Post Extraction
// Post data starts at index 1
// Date column: 5 ("Date Post Received")
// Weight column: 9 ("Post Purge Weight (grams)")
// Type column: 1 ("Type")
const postRows = postData.slice(1).filter(row => row && row[5] && isTargetPeriod(row[5]));

const totalFinishedOutputGrams = postRows.reduce((sum, row) => sum + (parseFloat(row[9]) || 0), 0);

// Average Yield Percent
// Yield = Total Output (g) / Total Input (g)
// Input is in lbs, need to convert to grams. 1 lb = 453.592 g
const totalBiomassGrams = totalBiomassLbs * 453.592;
let averageYieldPercent = 0;
if (totalBiomassGrams > 0) {
  averageYieldPercent = (totalFinishedOutputGrams / totalBiomassGrams) * 100;
}

// Post Processing Efficiency
// Let's assume this is (Post Purge Weight / Pre-Process Weight) * 100
// Pre-Process Weight is index 6
const totalPreProcessWeight = postRows.reduce((sum, row) => sum + (parseFloat(row[6]) || 0), 0);
let postProcessingEfficiency = 0;
if (totalPreProcessWeight > 0) {
  postProcessingEfficiency = (totalFinishedOutputGrams / totalPreProcessWeight) * 100;
}

// Active Production Days
// Count unique days in extraction + post extraction
const activeDays = new Set();
ffRows.forEach(row => activeDays.add(row[2]));
curedRows.forEach(row => activeDays.add(row[2]));
postRows.forEach(row => activeDays.add(row[5]));
const totalActiveDays = activeDays.size;


// Work in Progress
// Difference between extraction runs and post extraction entries?
// Or maybe "Transfered to Post" (TRUE) in extraction sheets vs entries in post extraction?
// Let's count items in FF/Cured that are marked "Transferred to Post" but NOT yet in Post Extraction list?
// That requires matching batch numbers.
// FF/Cured Batch Numbers (index 0) vs Post Batch Number (index 0).
// Note: Batch numbers might overlap between FF and Cured, so we should key by Type+Batch or just assume unique batch IDs if possible.
// Looking at data: FF has batches 2,5,6... Cured has 1,3,4... They seem interleaved/unique across types maybe?
// Let's check overlap.
// Actually, let's just count total "Transfered to Post" in FF+Cured for the month, and compare to total Post entries for the month?
// No, that's not accurate for WIP.
// WIP = (Total Extracted Batches ever - Total Post Processed Batches ever) ?
// Or simpler: Just count rows in FF/Cured where "Transfered to Post" is TRUE/Yes, and see if they exist in Post data?
// But wait, the prompt asks for "Work in progress" as a KPI.
// Let's look at the "Transfered to Post" column. If it says TRUE, it went to post.
// If it's in "post extraction", it's done (or at least entered there).
// Let's define WIP as: Batches extracted (in Feb) but NOT yet in Post Extraction list.
// We'll collect all batch IDs from FF/Cured that are "Transfered to Post" (or just extracted).
// Then check if they appear in Post Extraction.

const extractedBatches = [];
ffRows.forEach(row => extractedBatches.push({id: row[0], type: 'Fresh Frozen'}));
curedRows.forEach(row => extractedBatches.push({id: row[0], type: 'Cured'}));

const postBatches = new Set(postRows.map(row => row[0])); 
// Note: Post data only covers Feb. We should check ALL post data to see if a Feb batch was processed later?
// Or just check if it's in the current post list we pulled? 
// The prompt implies a monthly snapshot. If it's not in the post list (which we filtered for Feb), is it WIP?
// What if it was extracted in Feb but processed in March? Then it IS WIP for Feb report.
// So yes, compare Feb Extraction Batches vs Feb Post Batches.
// Actually, strictly speaking, WIP is anything currently in the system not finished.
// But based on available data, "Extracted in Feb but not Finished in Feb" is a good proxy for "New WIP added in Feb".
// Let's refine: "Total WIP" is hard without historical context.
// Let's stick to: "Batches extracted in Feb that are not in the Post Processing list for Feb".
// Wait, looking at data:
// FF Row 2: Batch 2, Date 2/18.
// Post Row 2: Batch 2, Type Fresh Frozen, Date 2/18.
// So match on ID.
// Let's filter the FULL post data (not just Feb) to check if batches are completed ever?
// Actually, I only have the full data in memory (I sliced it for calculations but loaded full file).
// So I will use `postData` (all rows) to check for completion.

const allPostBatches = new Set(postData.slice(1).map(row => row && row[0]));
let wipCount = 0;
extractedBatches.forEach(batch => {
  if (!allPostBatches.has(batch.id)) {
    wipCount++;
  }
});


// Compile Report Data
const report = {
  month: "February 2026",
  totalExtractionRuns,
  runsByMaterial: {
    freshFrozen: totalFFRuns,
    cured: totalCuredRuns
  },
  totalBiomassLbs,
  totalFinishedOutputGrams,
  averageYieldPercent: averageYieldPercent.toFixed(2),
  postProcessingEfficiency: postProcessingEfficiency.toFixed(2),
  activeProductionDays: totalActiveDays,
  workInProgress: wipCount
};

console.log(JSON.stringify(report, null, 2));

// Save to file for next step
fs.writeFileSync('kpi_report_data.json', JSON.stringify(report, null, 2));
