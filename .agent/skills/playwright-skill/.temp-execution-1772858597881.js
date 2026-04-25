const { chromium } = require('playwright');
const TARGET_URL = 'http://localhost:5173';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log(`Navigating to ${TARGET_URL}...`);
  await page.goto(TARGET_URL, { waitUntil: 'networkidle' });
  
  console.log('Testing flight search data fetch...');

  // Set Origin
  await page.click('text="출발지"');
  await page.fill('input[placeholder="국가, 도시 또는 공항"]', 'ICN');
  await page.waitForTimeout(500);
  await page.click('text="서울 인천"');
  
  // Set Destination
  await page.click('text="도착지"');
  await page.fill('input[placeholder="목적지 검색"]', 'LAX');
  await page.waitForTimeout(500);
  await page.click('text="로스앤젤레스"');

  // Submit search
  console.log('Submitting search...');
  await page.click('button:has-text("검색")');

  // Wait for results
  console.log('Waiting for results...');
  try {
     // Wait for either flight cards to appear or error text
     await Promise.race([
       page.waitForSelector('.flight-card:not(.flex-center)', { timeout: 15000 }),
       page.waitForSelector('text="API Error:"', { timeout: 15000 }),
       page.waitForSelector('text="검색된 일정에 부합하는"', { timeout: 15000 })
     ]);
     
     await page.waitForTimeout(1000); // Give it a sec to stabilize
     
     // Take a snapshot
     await page.screenshot({ path: 'd:/workspace_cli/skyscanner/search-result.png' });
     console.log('Screenshot saved to search-result.png');
     
     // Print results
     const resultText = await page.innerText('.flight-list');
     console.log('\n--- Flight Results Section ---');
     console.log(resultText);
     console.log('------------------------------\n');
     
  } catch (err) {
     console.error('Error waiting for results or parsing:', err.message);
  }
  
  await browser.close();
})();
