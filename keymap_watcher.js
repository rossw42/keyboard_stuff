// Simple keymap file watcher and parser
class KeymapWatcher {
    constructor() {
        this.keymapFiles = [
            'macropad/keymaps/default/keymap.c',
            '4x2/keymaps/2rows-with-encoder/keymap.c',
            'lily58/keymaps/default/keymap.c',
            'lily58/keymaps/lily58l/keymap.c',
            '4x2/keymaps/2rows-no-encoder/keymap.c',
            'lily58-hold/hold/keymaps/default/keymap.c'
        ];
        this.lastModified = {};
        this.updateInterval = 2000; // Check every 2 seconds
        this.init();
    }

    async init() {
        console.log('🎹 Keymap Watcher initialized');
        await this.checkForUpdates();
        setInterval(() => this.checkForUpdates(), this.updateInterval);
    }

    async checkForUpdates() {
        let hasChanges = false;
        
        for (const file of this.keymapFiles) {
            try {
                const response = await fetch(file + '?t=' + Date.now());
                if (response.ok) {
                    const lastModified = response.headers.get('last-modified');
                    if (this.lastModified[file] && this.lastModified[file] !== lastModified) {
                        console.log(`📝 Detected change in ${file}`);
                        hasChanges = true;
                    }
                    this.lastModified[file] = lastModified;
                }
            } catch (error) {
                // File might not exist or be accessible, that's ok
            }
        }

        if (hasChanges) {
            this.updateVisualization();
        }
    }

    async updateVisualization() {
        console.log('🔄 Updating keymap visualization...');
        const statusElement = document.getElementById('update-status');
        if (statusElement) {
            statusElement.textContent = 'Updating...';
            statusElement.className = 'update-status updating';
        }

        // Parse all keymap files and update the display
        await this.parseAllKeymaps();
        
        if (statusElement) {
            statusElement.textContent = 'Updated!';
            statusElement.className = 'update-status updated';
            setTimeout(() => {
                statusElement.textContent = 'Watching for changes...';
                statusElement.className = 'update-status';
            }, 2000);
        }
    }

    async parseAllKeymaps() {
        // This would parse the keymap files and update the DOM
        // For now, we'll just reload the page to keep it simple
        window.location.reload();
    }

    // Simple keymap parser for QMK files
    parseKeymap(content) {
        const layers = [];
        const keymapRegex = /const uint16_t PROGMEM keymaps\[\]\[MATRIX_ROWS\]\[MATRIX_COLS\] = \{([\s\S]*?)\};/;
        const match = content.match(keymapRegex);
        
        if (match) {
            const keymapContent = match[1];
            const layerRegex = /\[(\d+)\]\s*=\s*LAYOUT\(([\s\S]*?)\)/g;
            let layerMatch;
            
            while ((layerMatch = layerRegex.exec(keymapContent)) !== null) {
                const layerNum = parseInt(layerMatch[1]);
                const keys = layerMatch[2]
                    .split(',')
                    .map(key => key.trim().replace(/KC_/, ''))
                    .filter(key => key.length > 0);
                
                layers[layerNum] = keys;
            }
        }
        
        return layers;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new KeymapWatcher();
});