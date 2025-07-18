#!/usr/bin/env node

/**
 * Simple setup verification script for MR GIFT
 * Run with: node test-setup.js
 */

const fs = require('fs');
const path = require('path');

console.log('🎁 MR GIFT Setup Verification\n');

// Check if required files exist
const requiredFiles = [
  'mr-gift-app/.env',
  'backend/.env',
  'mr-gift-app/package.json',
  'backend/requirements.txt',
  'backend/app.py'
];

let allFilesExist = true;

console.log('📁 Checking required files...');
requiredFiles.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - Missing!`);
    allFilesExist = false;
  }
});

// Check environment variables
console.log('\n🔧 Checking environment configuration...');

function checkEnvFile(filePath, requiredVars) {
  if (!fs.existsSync(filePath)) {
    console.log(`❌ ${filePath} not found`);
    return false;
  }

  const envContent = fs.readFileSync(filePath, 'utf8');
  let allVarsSet = true;

  requiredVars.forEach(varName => {
    const regex = new RegExp(`^${varName}=(.+)$`, 'm');
    const match = envContent.match(regex);
    
    if (match && match[1] && !match[1].includes('your_') && !match[1].includes('_here')) {
      console.log(`✅ ${varName} is configured`);
    } else {
      console.log(`⚠️  ${varName} needs to be configured in ${filePath}`);
      allVarsSet = false;
    }
  });

  return allVarsSet;
}

const frontendEnvVars = [
  'VITE_CLERK_PUBLISHABLE_KEY',
  'VITE_STRIPE_PUBLISHABLE_KEY'
];

const backendEnvVars = [
  'CLERK_SECRET_KEY',
  'STRIPE_SECRET_KEY'
];

const frontendEnvOk = checkEnvFile('mr-gift-app/.env', frontendEnvVars);
const backendEnvOk = checkEnvFile('backend/.env', backendEnvVars);

// Summary
console.log('\n📋 Setup Summary:');
console.log(`Files: ${allFilesExist ? '✅' : '❌'}`);
console.log(`Frontend Config: ${frontendEnvOk ? '✅' : '⚠️'}`);
console.log(`Backend Config: ${backendEnvOk ? '✅' : '⚠️'}`);

if (allFilesExist && frontendEnvOk && backendEnvOk) {
  console.log('\n🎉 Setup looks good! You can start the application.');
  console.log('\nNext steps:');
  console.log('1. cd backend && python app.py');
  console.log('2. cd mr-gift-app && npm run dev');
  console.log('3. Open http://localhost:5173');
} else {
  console.log('\n⚠️  Setup incomplete. Please check the issues above.');
  console.log('Refer to SETUP.md for detailed instructions.');
}
