import { account } from '$lib/appwrite';
import { writable } from 'svelte/store';

const user = writable({})

// Function to handle logout action
export async function handleLogout() {
    // Implement logout logic here
    try {
        await account.deleteSession('current');
    } catch (error) {
        console.log(error);
    }

    user.set({});
    window.location.href = '../login';
}

async function getCurrentUser() {
    try {
        let loggedInUser = await account.get();
        user.set(loggedInUser);
    } catch (error) {
        // Pass
    }
}

getCurrentUser();

export default user