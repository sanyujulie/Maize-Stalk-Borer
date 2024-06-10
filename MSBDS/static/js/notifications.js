// Define an array of item types to check
const itemTypes = ['insurance', 'clients', 'ssl_certificates', 'domains', 'licenses', 'subscription' ]; // Add more item types as needed

// Function to check expiring items for a specific item type
function checkExpiringItems(itemType) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `/api/expiring_items/${itemType}/`,
            method: 'GET',
            success: function(data) {
                resolve({ itemType, data });
            },
            error: function(err) {
                reject(err);
            }
        });
    });
}

// Function to check expiring items for all specified item types
function checkAllExpiringItems() {
    const promises = itemTypes.map(itemType => checkExpiringItems(itemType));
    Promise.all(promises)
        .then(results => {
            const allNotifications = results.reduce((acc, { itemType, data }) => {
                return acc.concat(data.map(notification => ({
                    itemType,
                    // name: notification.name, // Change this based on your data structure
                    expiry_date: notification.expiry_date // Change this based on your data structure
                })));
            }, []);

            updateNotificationsDropdown(allNotifications);
        })
        .catch(error => {
            console.error('Error fetching expiring items:', error);
        })
        // .finally(() => {
        //     // Poll again after 5 seconds (or any desired interval)
        //     setTimeout(checkAllExpiringItems, 5000);
        // });
}

function updateNotificationsDropdown(notifications) {
    const dropdownMenu = $('.notifications');
    dropdownMenu.empty();

    if (notifications.length === 0) {
        dropdownMenu.append('<span class="dropdown-item text-center small text-gray-500">No expiring items found.</span>');
        $('#notification-count').text('0');
        return;
    }

    $('#notification-count').text(notifications.length);

    notifications.forEach(notification => {
        const formattedDate = new Date(notification.expiry_date).toLocaleDateString();

        const notificationItem = `
            <a class="dropdown-item d-flex align-items-center" href="/${notification.itemType}/">
                <div class="mr-3">
                    <div class="icon-circle bg-warning">
                        <i class="fas fa-exclamation-triangle text-white"></i>
                    </div>
                </div>
                <div>
                    <span style="color: rgb(255,255,255);">You have ${notification.itemType} expiring on ${formattedDate}</span>
                </div>
            </a>
        `;

        dropdownMenu.append(notificationItem);
    });
}

// Start polling when the user is logged in
if (userLoggedIn) {
    checkAllExpiringItems();
}
