import { put, get } from '@vercel/blob';

export const POST = async ({ request }) => {
  try {
    const newContact = await request.json();
    const blobName = 'contactos.json';
    let contacts = [];

    // Get the existing contacts blob and parse it as JSON
    const existingContacts = await get(blobName, { type: 'json' });

    if (existingContacts && Array.isArray(existingContacts)) {
      contacts = existingContacts;
    }

    // Add a timestamp to the new contact
    newContact.timestamp = new Date().toISOString();

    // Add new contact to the list
    contacts.push(newContact);

    // Upload the updated list to Vercel Blob
    await put(blobName, JSON.stringify(contacts, null, 2), {
      access: 'public',
      contentType: 'application/json',
    });

    return new Response(JSON.stringify({ message: 'Contact saved successfully' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Error in API route:', error);
    const errorMessage = error instanceof Error ? error.message : String(error);
    return new Response(JSON.stringify({ message: 'Error saving contact', error: errorMessage }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
