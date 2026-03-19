module.exports = {
  default: {
    require: [
      'features/support/**/*.ts',
      'features/step-definitions/**/*.ts'
    ],
    requireModule: [
      'ts-node/register',
      'tsconfig-paths/register'
    ],
    loader: ['ts-node/esm'],
    format: [
      'progress-bar',
      'json:reports/cucumber-report.json',
      'html:reports/cucumber-report.html'
    ],
    paths: ['features/**/*.feature'],
    publishQuiet: true
  }
};
