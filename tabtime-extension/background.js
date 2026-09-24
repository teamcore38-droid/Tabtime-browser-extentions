import { TabTimeStorage } from './storage.js';
import { createRuntime } from './browser-runtime.js';

createRuntime(chrome, new TabTimeStorage()).register();
