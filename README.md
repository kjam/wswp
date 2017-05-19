## Web Scraping with Python

Welcome to the code repository for [Web Scraping with Python, Second Edition]()! I hope you find the code and data here useful. If you have any questions reach out to @kjam on Twitter or GitHub.

### Code Structure

All of the code samples are in folders separated by chapter. Scripts are intended to be run from the `code` folder, allowing you to easily import from the chapters. 

### Code Examples

I have not included every code sample you've found in the book, but I have included a majority of the finished scripts. Although these are included, I encourage you to write out each code sample on your own and use these only as a reference.

### Firefox Issues

Depending on your version of Firefox and Selenium, you may run into JavaScript errors. Here are some fixes:
 * Use an older version of Firefox
 * Upgrade Selenium to >=3.0.2 and download the [geckodriver](https://github.com/mozilla/geckodriver/releases). Make sure the geckodriver is findable by your PATH variable. You can do this by adding this line to your `.bashrc` or `.bash_profile`. (Wondering what these are? Please read the Appendix C on learning the command line).
 * Use [PhantomJS](http://phantomjs.org/) with Selenium (change your browser line to `webdriver.PhantomJS('path/to/your/phantomjs/installation')`)
 * Use Chrome, InternetExplorer or any other [supported browser](http://www.seleniumhq.org/about/platforms.jsp)

Feel free to reach out if you have any questions!

### Corrections?

If you find any issues in these code examples, feel free to submit an Issue or Pull Request. I appreciate your input!


### First edition repository

If you are looking for the first edition's repository, you can find it here: [Web Scraping with Python, First Edition](https://bitbucket.org/wswp/)

### Questions?

Reach out to @kjam on Twitter or GitHub. @kjam is also often on freenode. :)
