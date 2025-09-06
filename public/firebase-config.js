// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDjVS0c7JmeVDDIIqzHIqvYJmhulmFbniw",
  authDomain: "excel-file-splitter-c75f8.firebaseapp.com",
  projectId: "excel-file-splitter-c75f8",
  storageBucket: "excel-file-splitter-c75f8.firebasestorage.app",
  messagingSenderId: "541934962971",
  appId: "1:541934962971:web:931118401cca71f63cabbe",
  measurementId: "G-GGGHL4VBY7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { app, analytics };
