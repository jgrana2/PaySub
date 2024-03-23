import { Client, Account, ID, Databases, Storage, Query } from 'appwrite';
import { config } from '$lib/config';

export const client = new Client();

// Use the PROJECT_ID from your .env file
client.setEndpoint('https://cloud.appwrite.io/v1').setProject(config.PROJECT_ID);

export const account = new Account(client);
const databases = new Databases(client);
const storage = new Storage(client);

// Set up the collection IDs as environment variables
const SUBSCRIPTIONS_COLLECTION_ID = config.SUBSCRIPTIONS_COLLECTION_ID;
const SUBSCRIBERS_COLLECTION_ID = config.SUBSCRIBERS_COLLECTION_ID;
const CARDS_COLLECTION_ID = config.CARDS_COLLECTION_ID;
const IMAGES_BUCKET_ID = config.IMAGES_BUCKET_ID;
const DATABASE_ID = config.DATABASE_ID;
const ACCESS_TOKENS_COLLECTION_ID = config.ACCESS_TOKENS_COLLECTION_ID;

export async function saveSubscription(data) {
    try {
        // Await the createDocument promise and store its result
        const response = await databases.createDocument(DATABASE_ID, SUBSCRIPTIONS_COLLECTION_ID, ID.unique(), data);
        // Use response here if needed
    } catch (error) {
        // Handle any errors that occur during the save operation
        console.error(error);
    }
}

export async function updateSubscription(data) {
    try {
        // Await the createDocument promise and store its result
        const response = await databases.updateDocument(DATABASE_ID, SUBSCRIPTIONS_COLLECTION_ID, data.$id, data);
        // Use response here if needed
    } catch (error) {
        // Handle any errors that occur during the save operation
        console.error(error);
    }
}

export async function updateSubscriber(data) {
    try {
        // Await the createDocument promise and store its result
        const response = await databases.updateDocument(DATABASE_ID, SUBSCRIBERS_COLLECTION_ID, data.$id, data);
        // Use response here if needed
    } catch (error) {
        // Handle any errors that occur during the save operation
        console.error(error);
    }
}

export async function saveCard(data) {
    try {
        // Await the createDocument promise and store its result
        const response = await databases.createDocument(DATABASE_ID, CARDS_COLLECTION_ID, ID.unique(), data);
        console.log("Card saved");
        // Use response here if needed
    } catch (error) {
        // Handle any errors that occur during the save operation
        console.error(error);
    }
}

export async function deleteCard(card) {
    try {
        // Await the createDocument promise and store its result
        const response = await databases.deleteDocument(DATABASE_ID, CARDS_COLLECTION_ID, card.$id);
        console.log("Card deleted");
        // Use response here if needed
    } catch (error) {
        // Handle any errors that occur during the save operation
        console.error(error);
    }
}

export async function getSubscriptions() {
    const promise = databases.listDocuments(DATABASE_ID, SUBSCRIPTIONS_COLLECTION_ID);

    return promise.then(function (response) {
        return response.documents; // Success
    }, function (error) {
        console.error(error); // Failure
        throw error;
    });
}

export async function getSubscribers() {
    const promise = databases.listDocuments(DATABASE_ID, SUBSCRIBERS_COLLECTION_ID);

    return promise.then(function (response) {
        return response.documents; // Success
    }, function (error) {
        console.error(error); // Failure
        throw error;
    });
}

export async function getCards() {
    const promise = databases.listDocuments(DATABASE_ID, CARDS_COLLECTION_ID);

    return promise.then(function (response) {
        return response.documents; // Success
    }, function (error) {
        console.error(error); // Failure
        throw error;
    });
}

export async function saveImageToBucket(file) {
    try {
        return storage.createFile(IMAGES_BUCKET_ID, ID.unique(), file);
    } catch (error) {
        console.error('Error uploading the file:', error);
        throw error;
    }
}

export async function getImage(id) {
    const result = storage.getFileView(IMAGES_BUCKET_ID, id);
    return result;
}

export async function register(firstname, lastname, phone, email, password) {
    try {
        try {
            await account.deleteSession('current');
        } catch (sessionError) {
            console.error('Failed to delete session:', sessionError);
        }

        // Create the account with email and password.
        const response = await account.create('unique()', email, password);

        // Login immediately
        const response_login = await account.createEmailSession(email, password);

        // Assuming response contains userId, use it to update additional information.
        const userId = response.$id;

        try {
            // Update name using Appwrite SDK, assuming a setName method exists.
            await account.updateName(`${firstname} ${lastname}`);
        } catch (nameError) {
            console.error('Error updating name:', nameError); // Log name update failure
        }

        // Format the phone number to start with +57
        const formattedPhone = `+57${phone}`;

        try {
            // Assuming an updatePhone method exists to update the user's phone number.
            await account.updatePhone(formattedPhone, password);
        } catch (phoneError) {
            console.error('Error updating phone:', phoneError); // Log phone update failure
        }

        alert('Cuenta creada con éxito');
        window.location.href = 'login';
    } catch (accountError) {
        console.error('Error registering user:', accountError);
        alert('Error registrando el usuario: ' + accountError.message);
    }
}

export async function saveAccessToken(data){
    try {
        // Await the createDocument promise and store its result
        const response = await databases.createDocument(DATABASE_ID, ACCESS_TOKENS_COLLECTION_ID, ID.unique(), data);
        console.log("Access token saved");
        // Use response here if needed
    } catch (error) {
        // Handle any errors that occur during the save operation
        console.error(error);
    }
}

export async function getAccessToken(data){
    const promise = databases.listDocuments(DATABASE_ID, ACCESS_TOKENS_COLLECTION_ID, [Query.limit(1)]);

    return promise.then(function (response) {
        return response.documents && response.documents.length > 0; // Success
    }, function (error) {
        console.error(error); // Failure
        throw error;
    });
}