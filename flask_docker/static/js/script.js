document.addEventListener("DOMContentLoaded", function() {
    // Add Profile Modal
    const addModal = document.getElementById("add-modal");
    const addProfileBtn = document.getElementById("add-profile");
    const closeBtn = document.getElementById("close");
    const addClass = document.getElementById("add-class-modal");
    const addClassBtn = document.getElementById("add-class");
    const closeClassBtn = document.getElementById("close-class");



   
    // Array of animal emojis
    const animalEmojis = [
        "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯",
        "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🦆", "🦅",
        "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌",
        "🐞", "🐜", "🦟", "🦗", "🕷️", "🦂", "🐢", "🐍", "🦎", "🦖",
        "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬",
        "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🐘",
        "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🐃", "🐂", "🐄", "🐎",
        "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🦮", "🐕‍🦺"
    ];
    
    // Function to get an emoji based on sub-account ID
    function getEmojiForAccount(subAccountId) {
        // Convert the sub-account ID to a number for deterministic selection
        let numericValue = 0;
        for (let i = 0; i < subAccountId.length; i++) {
            numericValue += subAccountId.charCodeAt(i);
        }
        
        // Use the numeric value to select an emoji from the array
        const index = numericValue % animalEmojis.length;
        return animalEmojis[index];
    }
    
    // Set emojis for all existing sub-accounts
    const profileEmojis = document.querySelectorAll('.profile-emoji[data-account-id]');
    profileEmojis.forEach(emoji => {
        const accountId = emoji.getAttribute('data-account-id');
        if (accountId) {
            emoji.textContent = getEmojiForAccount(accountId);
        }
    });
    
    // Function to get a random animal emoji for new accounts
    function getRandomAnimalEmoji() {
        const randomIndex = Math.floor(Math.random() * animalEmojis.length);
        return animalEmojis[randomIndex];
    }
    
    // Store selected emoji for form submission
    let selectedEmoji = getRandomAnimalEmoji();
    
    // Open add profile modal when the add profile button is clicked
    addProfileBtn.addEventListener("click", function() {
        // Generate a new random emoji each time modal is opened
        selectedEmoji = getRandomAnimalEmoji();
        
        // Update hidden emoji input field
        const emojiInput = document.getElementById("selected-emoji");
        if (emojiInput) {
            emojiInput.value = selectedEmoji;
        }
        
        // Preview the emoji in the modal
        const emojiPreview = document.getElementById("emoji-preview");
        if (emojiPreview) {
            emojiPreview.textContent = selectedEmoji;
        }
        
        addModal.style.display = "flex";
    });

    addClassBtn.addEventListener("click", function() {
        // Generate a new random emoji each time modal is opened
        selectedEmoji = getRandomAnimalEmoji();
        
        // Update hidden emoji input field
        const emojiInput = document.getElementById("selected-emoji-class");
        if (emojiInput) {
            emojiInput.value = selectedEmoji;
        }
        
        // Preview the emoji in the modal
        const emojiPreview = document.getElementById("emoji-class-preview");
        if (emojiPreview) {
            emojiPreview.textContent = selectedEmoji;
        }
        
        addClass.style.display = "flex";
    });

    closeClassBtn.addEventListener("click", function() {
        addClass.style.display = "none";
    });
    
    // Close add profile modal when clicking outside the modal
    window.addEventListener("click", function(event) {
        if (event.target === addClass) {
            addClass.style.display = "none";
        }
    });
    
    // Close add profile modal when the close button is clicked
    closeBtn.addEventListener("click", function() {
        addModal.style.display = "none";
    });
    
    // Close add profile modal when clicking outside the modal
    window.addEventListener("click", function(event) {
        if (event.target === addModal) {
            addModal.style.display = "none";
        }
    });
    
    // Manage Profiles Modal
    const manageModal = document.getElementById("manage-modal");
    
    // Close manage profiles modal when clicking outside the modal
    window.addEventListener("click", function(event) {
        if (event.target === manageModal) {
            manageModal.style.display = "none";
        }
    });
    
    // Initialize tabs
    const tabItems = document.querySelectorAll(".tab-item");
    tabItems.forEach(tab => {
        if (!tab.getAttribute("onclick")) {
            tab.addEventListener("click", function() {
                // For demonstration, we're only implementing "Delete a Profile"
                // Other tabs would just stay on the same screen
                alert("This feature is coming soon!");
            });
        }
    });
 });