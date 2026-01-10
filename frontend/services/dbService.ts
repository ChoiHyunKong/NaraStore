import {
    collection,
    addDoc,
    onSnapshot,
    query,
    orderBy,
    doc,
    updateDoc,
    serverTimestamp,
    deleteDoc,
    setDoc,
    where
} from 'firebase/firestore';
import { db } from '../firebase';
import { RFP, TodoItem } from '../types';

const RFP_COLLECTION = 'rfps';
const TODO_COLLECTION = 'todos';

export const dbService = {
    // --- RFP Operations ---

    // Real-time subscription to RFPs
    subscribeRFPs: (callback: (rfps: RFP[]) => void) => {
        const q = query(collection(db, RFP_COLLECTION), orderBy('createdAt', 'desc'));

        return onSnapshot(q, (snapshot) => {
            const rfps = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            })) as RFP[];
            callback(rfps);
        });
    },

    // Add new RFP
    addRFP: async (rfpData: Omit<RFP, 'id'>) => {
        return await addDoc(collection(db, RFP_COLLECTION), {
            ...rfpData,
            createdAt: serverTimestamp()
        });
    },

    // Update RFP status or results
    updateRFP: async (id: string, data: Partial<RFP>) => {
        const rfpRef = doc(db, RFP_COLLECTION, id);
        await updateDoc(rfpRef, data);
    },

    // Delete RFP and related Todos
    deleteRFP: async (id: string) => {
        // 1. Delete associated Todos first
        const todoQ = query(collection(db, TODO_COLLECTION), where('rfpId', '==', id));
        const snapshot = await import('firebase/firestore').then(mod => mod.getDocs(todoQ));

        const deletePromises = snapshot.docs.map(doc => deleteDoc(doc.ref));
        await Promise.all(deletePromises);

        // 2. Delete the RFP document
        await deleteDoc(doc(db, RFP_COLLECTION, id));
    },

    // --- Todo Operations ---

    // Real-time subscription to Todos for specific RFP
    subscribeTodos: (rfpId: string, callback: (todos: TodoItem[]) => void) => {
        const q = query(
            collection(db, TODO_COLLECTION),
            where('rfpId', '==', rfpId),
            orderBy('createdAt', 'desc')
        );

        return onSnapshot(q, (snapshot) => {
            const todos = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            })) as TodoItem[];
            callback(todos);
        });
    },

    // Real-time subscription to ALL Todos (Optimized for Dashboard)
    subscribeAllTodos: (callback: (todos: TodoItem[]) => void) => {
        const q = query(
            collection(db, TODO_COLLECTION),
            orderBy('createdAt', 'desc')
        );

        return onSnapshot(q, (snapshot) => {
            const todos = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            })) as TodoItem[];
            callback(todos);
        });
    },

    // Add Todo for specific RFP
    addTodo: async (rfpId: string, text: string) => {
        return await addDoc(collection(db, TODO_COLLECTION), {
            rfpId,
            text,
            completed: false,
            createdAt: serverTimestamp()
        });
    },

    // Toggle Todo Status
    toggleTodo: async (id: string, currentStatus: boolean) => {
        const todoRef = doc(db, TODO_COLLECTION, id);
        await updateDoc(todoRef, {
            completed: !currentStatus
        });
    },

    // Update Todo Text
    updateTodo: async (id: string, text: string) => {
        const todoRef = doc(db, TODO_COLLECTION, id);
        await updateDoc(todoRef, { text });
    },

    // Delete Todo
    deleteTodo: async (id: string) => {
        await deleteDoc(doc(db, TODO_COLLECTION, id));
    },

    // --- Personnel Operations ---

    subscribePersonnel: (callback: (personnel: import('../types').Personnel[]) => void) => {
        const q = query(collection(db, 'personnel'), orderBy('name', 'asc'));
        return onSnapshot(q, (snapshot) => {
            const personnel = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            })) as import('../types').Personnel[];
            callback(personnel);
        });
    },

    addPersonnel: async (person: Omit<import('../types').Personnel, 'id' | 'registeredAt'>) => {
        return await addDoc(collection(db, 'personnel'), {
            ...person,
            registeredAt: serverTimestamp()
        });
    },

    deletePersonnel: async (id: string) => {
        await deleteDoc(doc(db, 'personnel', id));
    }
};
