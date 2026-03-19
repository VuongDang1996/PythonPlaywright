const common = [
  'features/**/*.feature',                // Specify our feature files
  '--require-module ts-node/register',    // Load TypeScript module
  '--require features/**/*.ts',           // Load step definitions
  '--format progress-bar',                // Load custom formatter
  '--format json:reports/cucumber-report.json',
  '--format html:reports/cucumber-report.html',
  '--format @cucumber/pretty-formatter',
  '--publish-quiet'
].join(' ');

module.exports = {
  default: common,
  // More profiles can be added here
};
