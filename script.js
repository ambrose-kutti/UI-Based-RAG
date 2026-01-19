const API_BASE = window.location.origin; // Use same origin as served page
let currentDocumentId = null;
let currentDocumentName = null;
        // Show section
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(sectionId).classList.add('active'); // Show selected section
            document.getElementById('uploadStatus').innerHTML = ''; // Clear upload status when leaving upload section or when switching to any section
            if (sectionId !== 'upload') {   // Clear selected files when leaving upload section
                selectedFiles = [];
                document.getElementById('fileInput').value = '';
                document.getElementById('selectedFiles').style.display = 'none';
                document.getElementById('uploadProgress').style.display = 'none';
            }
            if (sectionId === 'documents') {    // Load documents if showing documents section
                loadDocuments();
            }
            if (sectionId === 'chatbot') {  // Clear chat input focus
                document.getElementById('chatInput').focus();
            }
        }
        // Upload file
        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const uploadBtn = document.getElementById('uploadBtn');
            const uploadStatus = document.getElementById('uploadStatus');
            if (!fileInput.files.length) {
                uploadStatus.innerHTML = '<div style="color: #e74c3c;">⚠️ Please select a file first</div>';
                return;
            }
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);
            uploadBtn.disabled = true;  // Disable button and show loading
            uploadBtn.innerHTML = '<span class="spinner"></span> Uploading...';
            uploadStatus.innerHTML = `
                <div style="background: #fff8e1; padding: 15px; border-radius: 8px; border-left: 4px solid #f39c12;">
                    <strong>📤 Uploading "${file.name}"...</strong>
                    <div style="margin-top: 8px; font-size: 14px; color: #7d6608;">
                        Processing: Extracting text → Storing document → Creating embeddings
                    </div>
                </div>
            `;
            try {
                const response = await fetch(`${API_BASE}/upload`, {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                if (result.status === 'success') {
                    uploadStatus.innerHTML = `
                        <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="font-size: 24px;">✅</span>
                                <div>
                                    <strong style="color: #155724;">Upload Successful!</strong>
                                    <div style="margin-top: 5px; color: #0c5460;">
                                        ${result.filename} uploaded successfully
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    fileInput.value = '';   // Clear file input
                    loadDocuments();    // Load updated documents
                } else {
                    uploadStatus.innerHTML = `
                        <div style="background: #f8d7da; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">
                            <strong style="color: #721c24;">Upload Failed</strong>
                            <div style="margin-top: 5px; color: #856404;">
                                ${result.message || 'Unknown error'}
                            </div>
                        </div>
                    `;
                }
            } catch (error) {
                uploadStatus.innerHTML = `
                    <div style="background: #f8d7da; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">
                        <strong style="color: #721c24;">Connection Error</strong>
                        <div style="margin-top: 5px; color: #856404;">
                            Make sure the backend server is running at http://localhost:8000
                        </div>
                    </div>
                `;
                console.error('Upload error:', error);
            } finally {
                uploadBtn.disabled = false; // Re-enable button
                uploadBtn.innerHTML = 'Upload Document';
            }
        }
        let selectedFiles = [];
        let uploadInProgress = false;
        document.getElementById('fileInput').addEventListener('change', function(e) {   // File selection handler
            selectedFiles = Array.from(e.target.files);
            displaySelectedFiles();
        });
        // Display selected files
        function displaySelectedFiles() {
            const fileList = document.getElementById('fileList');
            const selectedFilesDiv = document.getElementById('selectedFiles');
            const fileCount = document.getElementById('fileCount');
            const totalSize = document.getElementById('totalSize');
            
            if (selectedFiles.length > 0) {
                selectedFilesDiv.style.display = 'block';
                fileCount.textContent = selectedFiles.length;
                let totalBytes = 0;     // Calculate total size
                fileList.innerHTML = '';
                
                selectedFiles.forEach((file, index) => {
                    totalBytes += file.size;
                    
                    const fileItem = document.createElement('div');
                    fileItem.style.cssText = `
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center; 
                        padding: 8px 10px; 
                        margin-bottom: 5px; 
                        background: white; 
                        border-radius: 6px; 
                        border: 1px solid #dee2e6;
                    `;
                    fileItem.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 10px; flex: 1;">
                            <span style="font-size: 16px;">
                                ${file.type.includes('pdf') ? '📄' : '📝'}
                            </span>
                            <div style="flex: 1;">
                                <div style="font-weight: 500; font-size: 14px;">${file.name}</div>
                                <div style="font-size: 12px; color: #6c757d;">
                                    ${(file.size / 1024).toFixed(1)} KB
                                </div>
                            </div>
                        </div>
                        <button onclick="removeFile(${index})" 
                                style="background: #e74c3c; color: white; border: none; width: 24px; 
                                    height: 24px; border-radius: 50%; cursor: pointer; font-size: 12px;">
                            ×
                        </button>
                    `;
                    
                    fileList.appendChild(fileItem);
                });
                
                totalSize.textContent = (totalBytes / 1024).toFixed(1);
            } else {
                selectedFilesDiv.style.display = 'none';
            }
        }

        // Remove file from selection
        function removeFile(index) {
            selectedFiles.splice(index, 1);
            
            const dataTransfer = new DataTransfer();    // Update file input
            selectedFiles.forEach(file => dataTransfer.items.add(file));
            document.getElementById('fileInput').files = dataTransfer.files;
            
            displaySelectedFiles();
        }

        async function uploadMultipleFiles() {  // Upload multiple files
            if (selectedFiles.length === 0) {
                showUploadStatus(' Please select files first', 'warning');
                return;
            }
            
            if (uploadInProgress) {
                showUploadStatus(' Upload already in progress', 'warning');
                return;
            }
            
            const uploadBtn = document.getElementById('uploadBtn');
            const uploadProgress = document.getElementById('uploadProgress');
            const progressBar = document.getElementById('progressBar');
            const progressText = document.getElementById('progressText');
            const currentFile = document.getElementById('currentFile');
            // Disable upload button
            uploadInProgress = true;
            uploadBtn.disabled = true;
            uploadBtn.innerHTML = '<span class="spinner"></span> Uploading...';
            // Show progress
            uploadProgress.style.display = 'block';
            progressBar.style.width = '0%';
            progressText.textContent = `0/${selectedFiles.length}`;
            currentFile.textContent = 'Preparing upload...';
            // Show initial status
            showUploadStatus(`
                <div style="background: #fff8e1; padding: 15px; border-radius: 8px; border-left: 4px solid #f39c12;">
                    <strong> Starting upload of ${selectedFiles.length} files...</strong>
                    <div style="margin-top: 8px; font-size: 14px; color: #7d6608;">
                        Processing files in parallel for faster upload
                    </div>
                </div>
            `, 'info');
            try {
                const formData = new FormData();
                selectedFiles.forEach((file, index) => {    // Add all files to FormData
                    formData.append('files', file);
                });
                const response = await fetch(`${API_BASE}/upload-multiple`, { // Send request
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                progressBar.style.width = '100%';   // Update progress
                progressText.textContent = `${result.successful}/${selectedFiles.length}`;
                currentFile.textContent = 'Complete!';
                if (result.status === 'success' || result.status === 'partial') {
                    // Show success summary
                    let successHTML = `
                        <div style="background: #d4edda; padding: 20px; border-radius: 8px; border-left: 4px solid #28a745;">
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                                <span style="font-size: 24px;">✅</span>
                                <div>
                                    <strong style="color: #155724; font-size: 18px;">Upload Complete!</strong>
                                    <div style="color: #0c5460;">
                                        ${result.message}
                                    </div>
                                </div>
                            </div>
                    `;
                    if (result.successful > 0) {
                        successHTML += `
                            <div style="margin-top: 15px;">
                                <strong>Successfully uploaded:</strong>
                                <ul style="margin: 10px 0 0 20px; padding: 0;">
                        `;
                        result.successful_files.forEach(file => {
                            successHTML += `<li style="margin-bottom: 5px;">📄 ${file.filename}</li>`;
                        });
                        successHTML += `
                                </ul>
                            </div>
                        `;
                    }
                    if (result.failed > 0) {
                        successHTML += `
                            <div style="margin-top: 15px;">
                                <strong style="color: #856404;">Failed to upload:</strong>
                                <ul style="margin: 10px 0 0 20px; padding: 0;">
                        `;
                        result.failed_files.forEach(file => {
                            successHTML += `<li style="margin-bottom: 5px; color: #856404;">❌ ${file.filename}: ${file.error}</li>`;
                        });
                        successHTML += `
                                </ul>
                            </div>
                        `;
                    }
                    successHTML += `
                            <div style="margin-top: 15px; font-size: 14px; color: #6c757d;">
                                Processing time: ${result.processing_time}
                            </div>
                        </div>
                    `;
                    showUploadStatus(successHTML, 'success');
                    selectedFiles = []; // Clear selected files
                    document.getElementById('fileInput').value = '';
                    document.getElementById('selectedFiles').style.display = 'none';
                    loadDocuments();    // Load updated documents
                } else {
                    showUploadStatus(`
                        <div style="background: #f8d7da; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">
                            <strong style="color: #721c24;">Upload Failed</strong>
                            <div style="margin-top: 5px; color: #856404;">
                                ${result.message || 'Unknown error occurred'}
                            </div>
                        </div>
                    `, 'error');
                }
            } catch (error) {
                console.error('Upload error:', error);
                showUploadStatus(`
                    <div style="background: #f8d7da; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">
                        <strong style="color: #721c24;">Connection Error</strong>
                        <div style="margin-top: 5px; color: #856404;">
                            Make sure the backend server is running at http://localhost:8000
                        </div>
                    </div>
                `, 'error');
            } finally {
                uploadInProgress = false;   // Reset UI
                uploadBtn.disabled = false;
                uploadBtn.innerHTML = ' Upload';
                uploadProgress.style.display = 'none';
            }
        }

        // Helper function to show upload status
        function showUploadStatus(message, type = 'info') {
            const uploadStatus = document.getElementById('uploadStatus');
            uploadStatus.innerHTML = message;
            uploadStatus.scrollIntoView({ behavior: 'smooth', block: 'nearest' });  // Scroll to status
        }
        async function loadDocuments() {    // Load documents
        const documentList = document.getElementById('documentList');
        documentList.innerHTML = `
            <div style="text-align: center; padding: 30px;">
                <div class="spinner" style="border-top-color: #3498db; width: 40px; height: 40px; margin: 0 auto 15px;"></div>
                <p>Loading session documents...</p>
            </div>
        `;
        try {
            const response = await fetch(`${API_BASE}/ui-documents`);
            const result = await response.json();
            console.log('Loaded documents:', result); // Debug log
            if (result.status === 'success' && result.documents.length > 0) {
                documentList.innerHTML = '';
                document.getElementById('docCount').textContent = result.documents.length;  // Update document count
                result.documents.forEach(doc => {
                    const card = document.createElement('div');
                    card.className = 'document-card';
                    card.setAttribute('data-doc-id', doc.id);
                    card.innerHTML = `
                        <div class="document-header">
                            <div class="document-title">📄 ${doc.filename}</div>
                            <div style="font-size: 12px; color: #7f8c8d;">
                                ${new Date(doc.uploaded_at).toLocaleDateString()}
                            </div>
                        </div>
                        <div class="document-meta">
                            <div>Size: ${Math.ceil(doc.size / 1024)} KB</div>
                            <div style="margin-top: 5px; color: #95a5a6; font-size: 12px;">
                                ${doc.preview}
                            </div>
                        </div>
                        <div class="document-actions">
                            <button class="action-btn view-btn" onclick="viewDocument('${doc.id}', '${doc.filename.replace(/'/g, "\\'")}')">
                                View
                            </button>
                            <button class="action-btn edit-btn" onclick="editDocument('${doc.id}', '${doc.filename.replace(/'/g, "\\'")}')">
                                Edit
                            </button>
                            <button class="action-btn delete-btn" onclick="deleteDocument('${doc.id}', '${doc.filename.replace(/'/g, "\\'")}')">
                                Delete
                            </button>
                        </div>
                    `;
                    documentList.appendChild(card);
                });
                
                // Show session info
                const sessionInfo = document.createElement('div');
                sessionInfo.style.cssText = `
                    text-align: center; 
                    margin-top: 20px; 
                    padding: 10px; 
                    background: #f8f9fa; 
                    border-radius: 8px; 
                    font-size: 12px; 
                    color: #6c757d;
                `;
                sessionInfo.innerHTML = `
                    <div>Session ID: ${result.session_id || 'N/A'}</div>
                    <div>Documents in session: ${result.count} | Total in database: ${result.total_in_chromadb || 0}</div>
                `;
                documentList.appendChild(sessionInfo);
            } else {
                documentList.innerHTML = `
                    <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                        <div style="font-size: 48px; margin-bottom: 20px;">📁</div>
                        <h4>No documents in current session</h4>
                        <p>Upload documents to get started!</p>
                    </div>
                `;
                document.getElementById('docCount').textContent = '0';
            }
        } catch (error) {
            console.error('Load documents error:', error);
            documentList.innerHTML = `
                <div style="background: #f8d7da; padding: 20px; border-radius: 8px; text-align: center;">
                    <strong style="color: #721c24;"> Error loading documents</strong>
                    <div style="margin-top: 10px; color: #856404;">
                        ${error.message || 'Could not connect to the server'}
                    </div>
                </div>
            `;
        }
    }
        // View document
        async function viewDocument(docId, docName) {
            currentDocumentId = docId;
            currentDocumentName = docName;
            
            document.getElementById('viewModalTitle').textContent = `Viewing: ${docName}`;
            
            try {
                const response = await fetch(`${API_BASE}/ui-documents/${docId}`);
                const result = await response.json();
                if (result.status === 'success') {
                    const content = result.document.content;
                    document.getElementById('viewContent').textContent = content;
                    // Show modal
                    document.getElementById('viewModalOverlay').style.display = 'block';
                    document.getElementById('viewModal').style.display = 'block';
                } else {
                    alert('Error loading document: ' + result.message);
                }
            } catch (error) {
                alert('Error loading document');
                console.error('View document error:', error);
            }
        }

        // Close view modal
        function closeViewModal() {
            document.getElementById('viewModalOverlay').style.display = 'none';
            document.getElementById('viewModal').style.display = 'none';
            currentDocumentId = null;
            currentDocumentName = null;
        }

        // Edit document
        async function editDocument(docId, docName) {
            currentDocumentId = docId;
            currentDocumentName = docName;
            document.getElementById('editModalTitle').textContent = `Editing: ${docName}`;
            try {
                const response = await fetch(`${API_BASE}/ui-documents/${docId}`);
                const result = await response.json();
                if (result.status === 'success') {
                    document.getElementById('editContent').value = result.document.content;
                    // Show modal
                    document.getElementById('editModalOverlay').style.display = 'block';
                    document.getElementById('editModal').style.display = 'block';
                } else {
                    alert('Error loading document for editing: ' + result.message);
                }
            } catch (error) {
                alert('Error loading document');
                console.error('Edit document error:', error);
            }
        }

        // Close edit modal
        function closeEditModal() {
            // Reset save button first
            const saveBtn = document.querySelector('#editModal .save-btn');
            if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.innerHTML = 'Save Changes';
            }
            // Hide modal
            document.getElementById('editModalOverlay').style.display = 'none';
            document.getElementById('editModal').style.display = 'none';
            // Reset document tracking
            currentDocumentId = null;
            currentDocumentName = null;
        }

        // Save edited document
        async function saveDocument() {
            if (!currentDocumentId) return;
            const newContent = document.getElementById('editContent').value;
            const saveBtn = document.querySelector('#editModal .save-btn');
            // Disable save button
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<span class="spinner" style="border-top-color: white; width: 16px; height: 16px; margin-right: 5px;"></span> Saving...';
            try {
                const response = await fetch(`${API_BASE}/ui-documents/${currentDocumentId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ content: newContent })
                });
                const result = await response.json();
                if (result.status === 'success') {
                    closeEditModal();   // Close modal
                    loadDocuments();    // Reload documents
                    showToast('✅ Document saved successfully!', 'success');    // Show success message
                } else {
                    alert('Error saving document: ' + result.message);
                    resetSaveButton(saveBtn);   // RE-ENABLE THE BUTTON ON ERROR
                }
            } catch (error) {
                alert('Error saving document');
                console.error('Save document error:', error);
                resetSaveButton(saveBtn);   // RE-ENABLE THE BUTTON ON ERROR
            }
        }

        // Helper function to reset save button
        function resetSaveButton(saveBtn) {
            if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.innerHTML = 'Save Changes';
            }
        }

        // Delete document
        async function deleteDocument(docId, docName) {
            if (!confirm(`Are you sure you want to delete "${docName}" from current session?\nThis will also remove it from chatbot memory.`)) {
                return;
            }
            try {
                const response = await fetch(`${API_BASE}/ui-documents/${docId}`, {
                    method: 'DELETE'
                });
                const result = await response.json();
                if (result.status === 'success') {
                    // Remove the document card from UI immediately
                    const card = document.querySelector(`[data-doc-id="${docId}"]`);
                    if (card) {
                        card.style.opacity = '0.5';
                        card.style.transition = 'opacity 0.3s';
                        setTimeout(() => {
                            card.remove();
                            // Update document count
                            const remainingCards = document.querySelectorAll('.document-card').length;
                            document.getElementById('docCount').textContent = remainingCards;
                            // If no cards left, show empty message
                            if (remainingCards === 0) {
                                document.getElementById('documentList').innerHTML = `
                                    <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                                        <div style="font-size: 48px; margin-bottom: 20px;">📁</div>
                                        <h4>No documents in current session</h4>
                                        <p>Upload documents to get started!</p>
                                    </div>
                                `;
                            } 
                        }, 300);
                    }
                    showToast(` Document "${docName}" deleted successfully!`, 'success');
                    // Also trigger a full reload after a delay
                    setTimeout(() => {
                        loadDocuments();
                    }, 1000);
                } else {
                    showToast(` Error: ${result.message}`, 'error');
                }
            } catch (error) {
                console.error('Delete document error:', error);
                showToast(' Error deleting document. Please try again.', 'error');
            }
        }

        // Chat functions
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;
            const chatWindow = document.getElementById('chatWindow');
            // Add user message
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.textContent = message;
            chatWindow.appendChild(userMsg);
            input.value = '';   // Clear input
            // Add thinking indicator
            const thinkingMsg = document.createElement('div');
            thinkingMsg.className = 'message bot-message thinking';
            thinkingMsg.textContent = 'Thinking...';
            thinkingMsg.id = 'thinkingMsg';
            chatWindow.appendChild(thinkingMsg);
            chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to bottom
            try {
                const response = await fetch(`${API_BASE}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: message })
                });
                const result = await response.json();
                thinkingMsg.remove();   // Remove thinking message
                // Add bot response
                const botMsg = document.createElement('div');
                botMsg.className = 'message bot-message';
                // Format the answer with line breaks
                const formattedAnswer = result.answer.replace(/\n/g, '<br>');
                botMsg.innerHTML = formattedAnswer;
                chatWindow.appendChild(botMsg);
                chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to bottom
            } catch (error) {
                thinkingMsg.remove();   // Remove thinking message
                // Add error message
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message bot-message';
                errorMsg.textContent = 'Sorry, I encountered an error. Please try again.';
                chatWindow.appendChild(errorMsg);
                console.error('Chat error:', error);
            }
        }

        // Toast notification function
        function showToast(message, type = 'info') {
            // Remove existing toasts
            const existingToasts = document.querySelectorAll('.toast-notification');
            existingToasts.forEach(toast => toast.remove());
            const toast = document.createElement('div');
            toast.className = `toast-notification ${type}`;
            toast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 10000;
                animation: slideIn 0.3s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            `;
            if (type === 'success') {
                toast.style.background = 'linear-gradient(135deg, #27ae60, #219653)';
            } else if (type === 'error') {
                toast.style.background = 'linear-gradient(135deg, #e74c3c, #c0392b)';
            } else {
                toast.style.background = 'linear-gradient(135deg, #3498db, #2980b9)';
            }
            toast.textContent = message;
            document.body.appendChild(toast);
            // Auto remove after 3 seconds
            setTimeout(() => {
                toast.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    if (toast.parentNode) {
                        toast.parentNode.removeChild(toast);
                    }
                }, 300);
            }, 3000);
        }
        // Add CSS animations
        if (!document.querySelector('#toast-styles')) {
            const style = document.createElement('style');
            style.id = 'toast-styles';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
        // Enter key support for chat
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        // Load documents on page load
        window.onload = function() {
            loadDocuments();
            document.getElementById('chatInput').focus();   // Set focus to chat input if in chatbot section
        };
