<template>
  <div class="antialiased sans-serif bg-gray-200 w-screen h-screen">
    <div class="container mx-auto py-6 px-4">
      <h1 class="text-3xl py-4 border-b">Air Quality Datatable</h1>
      <div class="mb-4 flex justify-between items-center">
        <div class="flex-1 pr-4">
          <div class="relative md:w-1/3">
            <input
              class="w-full pl-10 pr-4 py-2 rounded-lg shadow focus:outline-none focus:shadow-outline text-gray-600 font-medium form-control"
              v-model="filter"
              type="search"
              placeholder="Search for city, country or location"
            />
            <div
              class="absolute top-0 left-0 inline-flex items-center p-2"
            ></div>
          </div>
        </div>
        <div>
          <div class="shadow rounded-lg flex">
            <div class="relative">
              <button
                @click.prevent="showToggle = !showToggle"
                class="rounded-lg inline-flex items-center bg-white hover:text-blue-500 focus:outline-none focus:shadow-outline text-gray-500 font-semibold py-2 px-2 md:px-4"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-6 h-6 md:hidden"
                  viewBox="0 0 24 24"
                  stroke-width="2"
                  stroke="currentColor"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <rect x="0" y="0" width="24" height="24" stroke="none"></rect>
                  <path
                    d="M5.5 5h13a1 1 0 0 1 0.5 1.5L14 12L14 19L10 16L10 12L5 6.5a1 1 0 0 1 0.5 -1.5"
                  />
                </svg>
                <span class="hidden md:block">Display</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5 ml-1"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  stroke-width="2"
                  stroke="currentColor"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <rect x="0" y="0" width="24" height="24" stroke="none"></rect>
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </button>

              <div
                v-show="showToggle"
                class="z-40 absolute top-0 right-0 w-40 bg-white rounded-lg shadow-lg mt-12 -mr-1 block py-1 overflow-hidden"
              >
                <template v-for="heading in headings" :key="heading.key">
                  <label
                    class="flex justify-start items-center text-truncate hover:bg-gray-100 px-4 py-2"
                  >
                    <div class="text-teal-600 mr-3">
                      <input
                        type="checkbox"
                        class="form-checkbox focus:outline-none focus:shadow-outline"
                        checked
                        @click="toggleColumn(heading.key)"
                      />
                    </div>
                    <div
                      class="select-none text-gray-700"
                      v-text="heading.value"
                    ></div>
                  </label>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="overflow-x-auto bg-white rounded-lg shadow overflow-y-auto relative"
        style="max-height: 70vh"
        v-on:scroll.passive="scroll"
      >
        <table
          class="border-collapse table-auto w-full whitespace-no-wrap bg-white table-striped relative"
        >
          <thead>
            <tr class="text-left">
              <template v-for="heading in headings" :key="heading.key">
                <th
                  class="py-2 px-3 sticky top-0 border-b border-gray-200 bg-gray-100"
                  :ref="heading.key"
                  :class="{ [heading.key]: true }"
                >
                  {{ heading.value }}
                </th>
              </template>
            </tr>
          </thead>
          <tbody>
            <tr
              class="hover:bg-gray-100"
              v-for="value in filteredItems"
              :key="value.id"
            >
              
              <td v-html="highlightMatches(value.city)" class="border-dashed border-t border-gray-200 city">
              </td>
              <td v-html="highlightMatches(value.country)" class="border-dashed border-t border-gray-200 country">
              </td>
              <td v-html="highlightMatches(value.location)" class="border-dashed border-t border-gray-200 location">
              </td>
              <td class="border-dashed border-t border-gray-200 pm25" :class="getPM25color(value.pm25)">
                {{ value.pm25 }}
              </td>
              <td class="border-dashed border-t border-gray-200 lastUpdated">
                {{ formatTime(value.lastUpdated) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filter: "",
      myObject: {},
      dataObject: {},
      computedObject: {},
      loadData: 50,
      headings: [
        {
          key: "city",
          value: "City",
        },
        {
          key: "country",
          value: "Country",
        },
        {
          key: "location",
          value: "Location",
        },
        {
          key: "pm25",
          value: "pm25 value",
        },
        {
          key: "lastUpdated",
          value: "Last Updated",
        },
      ],
      showToggle: false,
    };
  },
  computed: {
    
    filteredItems() {
      Object.filter = (obj, predicate) =>
        Object.keys(obj)
          .filter((key) => predicate(obj[key]))
          .reduce((res, key) => ((res[key] = obj[key]), res), {});
      
      return Object.filter(this.dataObject, (row) => ((row.city.toLowerCase().includes(this.filter.toLowerCase()) 
      || row.country.toLowerCase().includes(this.filter.toLowerCase())))).slice(9);
      
    },
  },
  mounted() {
    // ------------------------------------------
    //  HELPER FUNCTIONS
    // ------------------------------------------
    function checkStatus(response) {
      if (response.ok) {
        return Promise.resolve(response);
      } else {
        return Promise.reject(new Error(response.statusText));
      }
    }
    // ------------------------------------------
    //  FETCH FUNCTIONS
    // ------------------------------------------
    function fetchData(url) {
      return fetch(url, { mode: "cors" })
        .then(checkStatus)
        .then((res) => res.json())
        .catch((error) => console.log("Looks like there was a problem", error));
    }
    //http://127.0.0.1:5000/api/v1/datapoints
    //https://api.openaq.org/v1/latest
    fetchData("http://127.0.0.1:5000/api/v1/datapoints").then((data) => {
      this.dataObject = data.Datapoints;
    });
  },
  methods: {
      highlightMatches(text) {
    const matchExists = text.toLowerCase().includes(this.filter.toLowerCase());
    if (!matchExists) return text;

    const re = new RegExp(this.filter, 'ig');
    return text.replace(re, matchedText => `<strong>${matchedText}</strong>`);
  },
    getPM25value(pm25_value) {
      if(pm25_value == undefined){
        return "N/A"
      }

      return ;
    },
    getPM25color(pm25_value){
      if(pm25_value > 300){
        return "text-brown-600"
      }
      else if(pm25_value > 200){
        return "text-purple-600"
      }
      else if(pm25_value > 150){
        return "text-red-600"
      }
      else if(pm25_value > 100){
        return "text-orange-600"
      }
      else if(pm25_value > 50){
        return "text-yellow-600"
      }
      else if(pm25_value >= 0){
        return "text-green-600"
      }
      return ""
    },
    formatTime(timestring) {
      
      return timestring.substring(0, 10) + " " + timestring.substring(11, 19);
    },
    toggleColumn(key) {
      // Note: All td must have the same class name as the headings key!
      let columns = document.querySelectorAll("." + key);
      if (
        this.$refs[key].classList.contains("hidden") &&
        this.$refs[key].classList.contains(key)
      ) {
        columns.forEach((column) => {
          column.classList.remove("hidden");
        });
      } else {
        columns.forEach((column) => {
          column.classList.add("hidden");
        });
      }
    },
    loadMoreData(){
      
    },
      scroll (e) {
        
        /**
         * Function not finished yet
         * After scrolling to the bottom it should dynamically load more entries
         * -> achieve endless scrolling
         * Have to learn more about pagination
         */
        let bottomOfWindow = e.target.scrollHeight - e.target.scrollTop  <  e.target.clientHeight + 100

        if (bottomOfWindow) {
          this.loadMoreData();
        }
      }
  },
  
};
</script>