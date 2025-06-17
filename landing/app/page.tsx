export default function Home() {
  return (
    <div className="flex flex-col min-h-screen font-sans">
      {/* Hero Section */}
      <section className="flex flex-col md:flex-row items-center justify-between gap-8 container mx-auto px-4 py-20">
        <div className="md:w-1/2 space-y-4 text-center md:text-left">
          <h1 className="text-4xl font-bold">Plan Events with Confidence</h1>
          <p className="text-lg text-black">Find the best dates and avoid scheduling conflicts.</p>
        </div>
        <form className="md:w-1/2 bg-white shadow rounded p-6 space-y-4 w-full">
          <h2 className="text-xl font-semibold">Check Your Dates</h2>
          <input className="w-full border rounded p-2" type="text" placeholder="Event Name" />
          <select className="w-full border rounded p-2">
            <option value="">Event Type</option>
            <option>Conference</option>
            <option>Meetup</option>
            <option>Workshop</option>
          </select>
          <input className="w-full border rounded p-2" type="text" placeholder="Event Theme" />
          <div>
            <label className="block text-sm mb-1">Tentative Dates</label>
            <div className="flex gap-2">
              <input className="w-full border rounded p-2" type="date" />
              <input className="w-full border rounded p-2" type="date" />
            </div>
          </div>
          <input className="w-full border rounded p-2" type="text" placeholder="City" />
          <button type="submit" className="w-full bg-blue-600 text-white rounded p-2">Submit</button>
        </form>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold mb-8">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-2">
              <h3 className="font-semibold">1. Enter Details</h3>
              <p>Tell us about your event and preferred dates.</p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold">2. We Analyze</h3>
              <p>Our engine checks thousands of events for conflicts.</p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold">3. Pick Dates</h3>
              <p>Choose from the low-conflict dates we recommend.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Why It Matters */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold mb-8">Why It Matters</h2>
          <ul className="list-disc list-inside max-w-md mx-auto space-y-2 text-left">
            <li>Save time by avoiding date clashes.</li>
            <li>Improve attendance with optimal timing.</li>
            <li>Stay ahead of competing events.</li>
          </ul>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto py-8 bg-gray-800 text-gray-100 text-center space-y-2">
        <p>
          Contact: <a className="underline" href="mailto:kamil@kamilvitek.cz">kamil@kamilvitek.cz</a>
        </p>
        <p>
          <a className="underline" href="https://www.linkedin.com/in/kamil-vitek" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        </p>
      </footer>
    </div>
  );
}
