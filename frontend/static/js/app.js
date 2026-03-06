// NanoShop - Frontend Application

class NanoShop {
    constructor() {
        this.sessionId = null;
        this.currentImage = null;
        this.originalImage = null;
        this.operations = [];
        this.isComparing = false;
        this.zoom = 1;
        this.exportFormat = 'png';

        this.initElements();
        this.initEventListeners();
    }

    initElements() {
        // Upload elements
        this.uploadZone = document.getElementById('uploadZone');
        this.fileInput = document.getElementById('fileInput');
        this.imageDisplay = document.getElementById('imageDisplay');
        this.currentImageEl = document.getElementById('currentImage');
        this.originalImageEl = document.getElementById('originalImage');
        this.canvasActions = document.getElementById('canvasActions');
        this.operationsPanel = document.getElementById('operationsPanel');
        this.operationsList = document.getElementById('operationsList');

        // Chat elements
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.suggestions = document.getElementById('suggestions');
        this.chatStatus = document.getElementById('chatStatus');

        // Control buttons
        this.resetBtn = document.getElementById('resetBtn');
        this.exportBtn = document.getElementById('exportBtn');
        this.compareBtn = document.getElementById('compareBtn');
        this.zoomInBtn = document.getElementById('zoomInBtn');
        this.zoomOutBtn = document.getElementById('zoomOutBtn');
        this.resetViewBtn = document.getElementById('resetViewBtn');
        this.undoBtn = document.getElementById('undoBtn');

        // Modal
        this.exportModal = document.getElementById('exportModal');
        this.closeExportModal = document.getElementById('closeExportModal');
        this.cancelExport = document.getElementById('cancelExport');
        this.confirmExport = document.getElementById('confirmExport');
        this.formatBtns = document.querySelectorAll('.format-btn');

        // Toast
        this.toast = document.getElementById('toast');
    }

    initEventListeners() {
        // Upload
        this.uploadZone.addEventListener('click', () => this.fileInput.click());
        this.uploadZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadZone.addEventListener('dragleave', () => this.uploadZone.classList.remove('dragover'));
        this.uploadZone.addEventListener('drop', (e) => this.handleDrop(e));
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Chat
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Suggestion chips
        document.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                this.chatInput.value = chip.dataset.prompt;
                this.sendMessage();
            });
        });

        // Canvas controls
        this.resetBtn.addEventListener('click', () => this.resetImage());
        this.exportBtn.addEventListener('click', () => this.showExportModal());
        this.compareBtn.addEventListener('click', () => this.toggleCompare());
        this.zoomInBtn.addEventListener('click', () => this.zoomIn());
        this.zoomOutBtn.addEventListener('click', () => this.zoomOut());
        this.resetViewBtn.addEventListener('click', () => this.resetView());
        this.undoBtn.addEventListener('click', () => this.undo());

        // Modal
        this.closeExportModal.addEventListener('click', () => this.hideExportModal());
        this.cancelExport.addEventListener('click', () => this.hideExportModal());
        this.confirmExport.addEventListener('click', () => this.exportImage());
        this.formatBtns.forEach(btn => {
            btn.addEventListener('click', () => this.selectFormat(btn));
        });

        // Modal backdrop
        this.exportModal.querySelector('.modal-backdrop').addEventListener('click', () => this.hideExportModal());
    }

    // Upload handling
    handleDragOver(e) {
        e.preventDefault();
        this.uploadZone.classList.add('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.uploadFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.uploadFile(file);
        }
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        this.showToast('Uploading image...', 'info');

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.sessionId = data.session_id;
                this.currentImage = data.image;
                this.originalImage = data.image;
                this.operations = [];

                this.displayImage(data.image);
                this.enableChat(data.message);
                this.showToast('Image uploaded!', 'success');
            } else {
                this.showToast(data.error || 'Upload failed', 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showToast('Failed to connect to server', 'error');
        }
    }

    displayImage(base64) {
        const imageUrl = `data:image/png;base64,${base64}`;

        this.uploadZone.classList.add('hidden');
        this.imageDisplay.classList.remove('hidden');
        this.canvasActions.classList.remove('hidden');
        this.operationsPanel.classList.remove('hidden');
        this.suggestions.classList.remove('hidden');

        this.currentImageEl.src = imageUrl;
        this.originalImageEl.src = imageUrl;
    }

    enableChat(welcomeMessage) {
        this.chatInput.disabled = false;
        this.sendBtn.disabled = false;

        // Clear welcome message and add AI welcome
        this.chatMessages.innerHTML = '';
        this.addMessage('assistant', welcomeMessage);
    }

    // Chat handling
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || !this.sessionId) return;

        // Add user message
        this.addMessage('user', message);
        this.chatInput.value = '';

        // Show typing indicator
        const typingId = this.addTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    message: message
                })
            });

            const data = await response.json();
            this.removeTypingIndicator(typingId);

            if (data.success) {
                this.addMessage('assistant', data.message);

                // Show suggested operations
                if (data.suggested_operations && data.suggested_operations.length > 0) {
                    this.showSuggestedOperations(data.suggested_operations);
                }
            } else {
                this.addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator(typingId);
            this.addMessage('assistant', 'Failed to connect to AI. Please try again.');
        }
    }

    addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const avatarSvg = role === 'user'
            ? '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>'
            : '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>';

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    ${avatarSvg}
                </svg>
            </div>
            <div class="message-content">${content}</div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = id;
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
            </div>
            <div class="message-content">
                <span class="typing-dots">
                    <span></span><span></span><span></span>
                </span>
            </div>
        `;

        this.chatMessages.appendChild(typingDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

        // Add typing animation
        const style = document.createElement('style');
        style.textContent = `
            .typing-dots { display: flex; gap: 4px; }
            .typing-dots span {
                width: 8px; height: 8px; background: var(--text-secondary);
                border-radius: 50%; animation: typing 1.4s infinite;
            }
            .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
            .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
            @keyframes typing {
                0%, 100% { opacity: 0.3; }
                50% { opacity: 1; }
            }
        `;
        document.head.appendChild(style);

        return id;
    }

    removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    showSuggestedOperations(operations) {
        const lastMessage = this.chatMessages.lastElementChild;
        if (!lastMessage) return;

        const opsContainer = document.createElement('div');
        opsContainer.className = 'suggested-ops';

        operations.forEach(op => {
            const btn = document.createElement('button');
            btn.className = 'suggested-op-btn';
            btn.textContent = `${this.formatOperationName(op.type)} (${op.value.toFixed(1)})`;
            btn.addEventListener('click', () => this.applyOperation(op));
            opsContainer.appendChild(btn);
        });

        lastMessage.appendChild(opsContainer);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    formatOperationName(type) {
        return type.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    // Operation handling
    async applyOperation(operation) {
        try {
            const response = await fetch('/api/apply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    operation: operation.type,
                    value: operation.value
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentImage = data.image;
                this.currentImageEl.src = `data:image/png;base64,${data.image}`;
                this.operations.push(operation);
                this.updateOperationsList();
                this.showToast(`Applied ${this.formatOperationName(operation.type)}!`, 'success');
            } else {
                this.showToast(data.error || 'Failed to apply operation', 'error');
            }
        } catch (error) {
            console.error('Apply error:', error);
            this.showToast('Failed to apply operation', 'error');
        }
    }

    updateOperationsList() {
        this.operationsList.innerHTML = '';

        this.operations.forEach((op, index) => {
            const card = document.createElement('div');
            card.className = 'operation-card';
            card.innerHTML = `
                <span>${this.formatOperationName(op.type)}</span>
                <button class="remove-btn" data-index="${index}">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            `;

            card.querySelector('.remove-btn').addEventListener('click', () => {
                this.removeOperation(index);
            });

            this.operationsList.appendChild(card);
        });
    }

    async removeOperation(index) {
        // Undo all operations after this index
        const toRemove = this.operations.length - 1 - index;
        for (let i = 0; i < toRemove; i++) {
            await this.undo();
        }
    }

    // Image controls
    async resetImage() {
        if (!this.sessionId) return;

        try {
            const response = await fetch('/api/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });

            const data = await response.json();

            if (data.success) {
                this.currentImage = data.image;
                this.currentImageEl.src = `data:image/png;base64,${data.image}`;
                this.originalImageEl.src = `data:image/png;base64,${data.image}`;
                this.operations = [];
                this.updateOperationsList();
                this.showToast('Image reset to original', 'success');
            }
        } catch (error) {
            console.error('Reset error:', error);
            this.showToast('Failed to reset image', 'error');
        }
    }

    async undo() {
        if (!this.sessionId || this.operations.length === 0) return;

        try {
            const response = await fetch('/api/undo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });

            const data = await response.json();

            if (data.success) {
                this.currentImage = data.image;
                this.currentImageEl.src = `data:image/png;base64,${data.image}`;
                this.operations.pop();
                this.updateOperationsList();
                this.showToast('Undone', 'success');
            }
        } catch (error) {
            console.error('Undo error:', error);
        }
    }

    toggleCompare() {
        this.isComparing = !this.isComparing;
        if (this.isComparing) {
            this.originalImageEl.classList.remove('hidden');
            this.currentImageEl.classList.add('hidden');
        } else {
            this.originalImageEl.classList.add('hidden');
            this.currentImageEl.classList.remove('hidden');
        }
    }

    zoomIn() {
        this.zoom = Math.min(this.zoom * 1.2, 3);
        this.currentImageEl.style.transform = `scale(${this.zoom})`;
    }

    zoomOut() {
        this.zoom = Math.max(this.zoom / 1.2, 0.5);
        this.currentImageEl.style.transform = `scale(${this.zoom})`;
    }

    resetView() {
        this.zoom = 1;
        this.currentImageEl.style.transform = 'scale(1)';
    }

    // Export
    showExportModal() {
        this.exportModal.classList.remove('hidden');
    }

    hideExportModal() {
        this.exportModal.classList.add('hidden');
    }

    selectFormat(btn) {
        this.formatBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.exportFormat = btn.dataset.format;
    }

    async exportImage() {
        if (!this.sessionId) return;

        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    format: this.exportFormat
                })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `nanoshop_export.${this.exportFormat}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);

                this.hideExportModal();
                this.showToast('Image exported!', 'success');
            } else {
                this.showToast('Export failed', 'error');
            }
        } catch (error) {
            console.error('Export error:', error);
            this.showToast('Failed to export image', 'error');
        }
    }

    // Toast
    showToast(message, type = 'info') {
        this.toast.className = `toast ${type}`;
        this.toast.querySelector('.toast-message').textContent = message;
        this.toast.classList.remove('hidden');

        setTimeout(() => {
            this.toast.classList.add('hidden');
        }, 3000);
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    window.nanoShop = new NanoShop();
});
