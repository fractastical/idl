
let userId = "";

const firebaseConfig = {
    apiKey: "AIzaSyCvgdn8c6D8RusKRr4vHAzFj1x4FNxrXVE",
    authDomain: "infinite-games-9c69e.firebaseapp.com",
    projectId: "infinite-games-9c69e",
    storageBucket: "infinite-games-9c69e.appspot.com",
    messagingSenderId: "602022483888",
    appId: "1:602022483888:web:f967a6c1cb236ae66ba875",
    measurementId: "G-9LE6E1BKZ7"
};


import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc, updateDoc, collection, getDocs } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";


// Firebase configuration and initialization
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);

document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    auth.signInWithEmailAndPassword(email, password)
        .then(userCredential => {
            const user = userCredential.user;
            loadUserData(user.uid);
        })
        .catch(error => {
            console.error("Error signing in:", error.message);
        });
});

auth.onAuthStateChanged(user => {
    if (user) {
        loadUserData(user.uid);
        userId = user.uid;
    } else {
        document.getElementById('user-info').classList.add('hidden');
        document.getElementById('login-link').classList.remove('hidden');
    }
});

async function loadUserData(userId) {
    try {
        const userDoc = await getDoc(doc(db, 'users', userId));

        // const userDoc = await db.doc(`users/${userId}`).get();
        if (userDoc.exists) {
            const userData = userDoc.data();
            document.getElementById('user-nickname').textContent = userData.nickname;
            document.getElementById('user-coins').textContent = userData.coins;
            document.getElementById('user-info').classList.remove('hidden');
            document.getElementById('login-link').classList.add('hidden');
            document.getElementById('auth').classList.add('hidden');
            document.getElementById('game-section').classList.remove('hidden');
            console.log("pizza");
            // saveUserData(userId);

        } else {
            console.log("No such document!");
        }
    } catch (error) {
        console.error("Error getting user data:", error);
    }
}

document.getElementById('login-toggle').addEventListener('click', function (event) {
    event.preventDefault();
    document.getElementById('auth').classList.toggle('hidden');
});



// Function to save user score for a specific game
async function saveUserScore(userId, gameName, score) {
    const userDocRef = doc(db, 'users', userId);
    const sessionLength = calculateSessionLength(); // Implement this function as needed
    const loginTime = new Date();

    // Save the score, session length, and login time for the specific game
    const gameData = {
        [`games.${gameName}.scores`]: arrayUnion({
            score: score,
            sessionLength: sessionLength,
            loginTime: loginTime
        })
    };

    await updateDoc(userDocRef, gameData);
}

window.saveUserScore = saveUserScore;

// Function to save initial user data
async function saveUserData(userId, gameName) {
    const userData = {
        [`games.${gameName}`]: {
            scores: [],
            lastLogin: new Date(),
            pizza: "pizza" // Sample data, adjust as needed
        }
    };
    await updateDoc(doc(db, 'users', userId), userData);
}

window.saveUserData = saveUserData;

// Function to load leaderboard for a specific game
async function loadLeaderboard(gameName) {
    const usersSnapshot = await getDocs(collection(db, 'users'));
    const users = [];

    usersSnapshot.forEach(doc => {
        const userData = doc.data();
        const gameScores = userData.games?.[gameName]?.scores || [];
        const highestScore = gameScores.reduce((max, session) => Math.max(max, session.score), 0);
        
        users.push({
            nickname: userData.nickname || 'Unnamed',
            score: highestScore
        });
    });

    users.sort((a, b) => b.score - a.score);
    const topUsers = users.slice(0, 10);

    const leaderboard = document.createElement('div');
    leaderboard.innerHTML = `<h2>Leaderboard for ${gameName}</h2>`;
    topUsers.forEach((user, index) => {
        const userDiv = document.createElement('div');
        userDiv.innerText = `${index + 1}. ${user.nickname}: ${user.score} points`;
        leaderboard.appendChild(userDiv);
    });

    document.getElementById('result').appendChild(leaderboard);
}

window.loadLeaderboard = loadLeaderboard;

// Function to calculate session length (to be implemented as needed)
function calculateSessionLength() {
    // Placeholder implementation
    return Math.floor(Math.random() * 1000); // Replace with actual session length calculation
}
