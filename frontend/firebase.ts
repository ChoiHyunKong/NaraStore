import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
    projectId: "narastore-analytics",
    appId: "1:650575683418:web:81ad16a720da1ae1695d63",
    storageBucket: "narastore-analytics.firebasestorage.app",
    apiKey: "AIzaSyA7WP46JlxKKdwPxOQywTI7I9FlvbM7Ibk",
    authDomain: "narastore-analytics.firebaseapp.com",
    messagingSenderId: "650575683418"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
