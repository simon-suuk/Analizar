/**
 *
 * @Author       Created by draogtech on 29/06/17 using Webstorm.
 * @Time         :2/24/18 00:19
 * @Copyright (C) 2018$
 *
 */

const puppeteer = require('puppeteer');

async function run() {
   const browser = await puppeteer.launch({
                                             headless: false
                                          });
   const page = await browser.newPage();
   await page.goto('https://likealyzer.com');
   await page.screenshot({ path: 'screenshots/likealyzer.png' });

   const userToSearch = 'draogsport';
   const searchUrl = `https://likealyzer.com/report/488337748018557/?q=${userToSearch}`;

   await page.goto(searchUrl);
   await page.waitFor(2 * 1000);

   const LIKEALYZER_OVERVIEW_INFO = '#__next > div > div > div > div.css-m4ifhj > div.css-1bpkqsf > div:nth-child(1) > div                                    > div.css-yt7b0r > div.css-18tgnnw > div.css-1t62idy > ul > li:nth-child(INDEX)';

   const LENGTH_SELECTOR_CLASS = 'css-6w6u3k';

   let listLength = await page.evaluate((sel) => {
      return document.getElementsByClassName(sel).length;
   }, LENGTH_SELECTOR_CLASS);
   

   console.log(listLength);

   for (let i = 1; i <= listLength; i++) {
      // change the index to the next child
      let overview_info_selector = LIKEALYZER_OVERVIEW_INFO.replace("INDEX", i);

      let overview_info= await page.evaluate((sel) => {
         let element = document.querySelector(sel);
      return element ? element.innerHTML : null;
   }, overview_info_selector);

      console.log(overview_info);

   }

   browser.close();
}





run();

