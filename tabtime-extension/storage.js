import { addToSummary, emptySummary } from './tracking-core.js';

const DB_NAME = 'TabTimeDB';
const DB_VERSION = 2;
const SESSIONS = 'sessions';
const SUMMARIES = 'daily_summaries';
const META = 'metadata';

export class TabTimeStorage {
  constructor(dbName = DB_NAME) {
    this.dbName = dbName;
    this.opening = null;
  }

  initDB() {
    if (this.opening) return this.opening;
    this.opening = new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, DB_VERSION);
      request.onupgradeneeded = () => {
        const db = request.result;
        const tx = request.transaction;
        if (!db.objectStoreNames.contains(SESSIONS)) {
          const store = db.createObjectStore(SESSIONS, { keyPath: 'id', autoIncrement: true });
          for (const key of ['domain', 'date', 'category']) store.createIndex(key, key);
        }
        if (!db.objectStoreNames.contains(SUMMARIES)) db.createObjectStore(SUMMARIES, { keyPath: 'date' });
        if (!db.objectStoreNames.contains(META)) db.createObjectStore(META, { keyPath: 'key' });
        // Preserve v1 session records and rebuild the previously unused daily rollups.
        const summaries = new Map();
        const cursor = tx.objectStore(SESSIONS).openCursor();
        cursor.onsuccess = () => {
          const row = cursor.result;
          if (row) {
            const record = row.value;
            if (record.date && record.domain) {
              const summary = summaries.get(record.date) || emptySummary(record.date);
              summaries.set(record.date, addToSummary(summary, record));
            }
            row.continue();
          } else {
            const store = tx.objectStore(SUMMARIES);
            store.clear();
            for (const summary of summaries.values()) store.put(summary);
          }
        };
      };
      request.onsuccess = () => {
        const db = request.result;
        db.onversionchange = () => { db.close(); this.opening = null; };
        resolve(db);
      };
      request.onerror = () => { this.opening = null; reject(request.error); };
      request.onblocked = () => { console.warn('Tab Time database upgrade is waiting for another extension page to close.'); };
    });
    return this.opening;
  }

  async read(storeName, key, indexName) {
    const db = await this.initDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(storeName, 'readonly');
      const store = tx.objectStore(storeName);
      const request = indexName ? store.index(indexName).getAll(key) : key === undefined ? store.getAll() : store.get(key);
      tx.oncomplete = () => resolve(request.result);
      tx.onabort = () => reject(tx.error || new Error('Storage read aborted'));
      tx.onerror = () => reject(tx.error);
    });
  }

  async getTrackingState() {
    return (await this.read(META, 'tracking'))?.value || null;
  }

  async getDaySummary(date) {
    return await this.read(SUMMARIES, date) || emptySummary(date);
  }

  async commitTracking(records, state) {
    const db = await this.initDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction([SESSIONS, SUMMARIES, META], 'readwrite');
      const sessions = tx.objectStore(SESSIONS);
      const summaries = tx.objectStore(SUMMARIES);
      const byDate = Map.groupBy ? Map.groupBy(records, record => record.date) : records.reduce((map, record) => {
        if (!map.has(record.date)) map.set(record.date, []);
        map.get(record.date).push(record);
        return map;
      }, new Map());
      // Inserts (not puts) reject a repeated interval; the entire transaction then rolls back.
      for (const record of records) sessions.add(record);
      for (const [date, dailyRecords] of byDate) {
        const request = summaries.get(date);
        request.onsuccess = () => {
          const summary = request.result || emptySummary(date);
          for (const record of dailyRecords) addToSummary(summary, record);
          summaries.put(summary);
        };
      }
      tx.objectStore(META).put({ key: 'tracking', value: state });
      tx.oncomplete = () => resolve();
      tx.onabort = () => reject(tx.error || new Error('Tracking transaction aborted'));
      tx.onerror = () => reject(tx.error || new Error('Tracking write failed'));
    });
  }

  getSessionsByDate(date) { return this.read(SESSIONS, date, 'date'); }
  getAllSessions() { return this.read(SESSIONS); }

  async clearAllData() {
    const db = await this.initDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction([SESSIONS, SUMMARIES, META], 'readwrite');
      for (const name of [SESSIONS, SUMMARIES, META]) tx.objectStore(name).clear();
      tx.oncomplete = () => resolve(true);
      tx.onabort = () => reject(tx.error || new Error('History deletion aborted'));
      tx.onerror = () => reject(tx.error);
    });
  }
}

// Default domain categorization rules
export const DEFAULT_CATEGORY_RULES = {
  // Productive
  'github.com': 'Productive',
  'gitlab.com': 'Productive',
  'stackoverflow.com': 'Productive',
  'docs.google.com': 'Productive',
  'notion.so': 'Productive',
  'slack.com': 'Productive',
  'trello.com': 'Productive',
  'figma.com': 'Productive',
  'codepen.io': 'Productive',
  'chatgpt.com': 'Productive',
  
  // Educational
  'sciencedirect.com': 'Educational',
  'ieeexplore.ieee.org': 'Educational',
  'acm.org': 'Educational',
  'researchgate.net': 'Educational',
  'jstor.org': 'Educational',
  'yorksj.ac.uk': 'Educational',
  'moodle.org': 'Educational',
  'khanacademy.org': 'Educational',
  'coursera.org': 'Educational',
  'edx.org': 'Educational',
  'wikipedia.org': 'Educational',

  // Social
  'twitter.com': 'Social',
  'x.com': 'Social',
  'facebook.com': 'Social',
  'instagram.com': 'Social',
  'reddit.com': 'Social',
  'linkedin.com': 'Social',
  'tiktok.com': 'Social',
  'discord.com': 'Social',

  // Entertainment
  'youtube.com': 'Entertainment',
  'netflix.com': 'Entertainment',
  'twitch.tv': 'Entertainment',
  'spotify.com': 'Entertainment',
  'disneyplus.com': 'Entertainment',
  'primevideo.com': 'Entertainment'
};

export const DEFAULT_BLOCKLIST = [
  'twitter.com',
  'x.com',
  'facebook.com',
  'instagram.com',
  'reddit.com',
  'tiktok.com',
  'netflix.com',
  'twitch.tv'
];
