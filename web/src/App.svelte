<script>
import * as d3 from  "d3";
import * as color from "./color.js";

const lowFreq = 380;
const highFreq = 780;
const freqStep = 5;
const NUM_IMAGES = 359;

function _freqs() {
	let res = [lowFreq];
	let f = lowFreq
	while(f < highFreq) {
		res.push(f+=freqStep);
	}
	return res;
}
const freqs = _freqs();

let data = "Loading...";
let sample_idx = 0;

async function getData() {
	const data = await d3.csv("data/reflectances.csv", (r) => {
		let freq_to_label = (f) => {
			if(f == 380) {
				return '380 [nm]';
			} else {
				return '' + f;
			}};
		let radiances = [];
		radiances = radiances.concat(...freqs.map(i => r[freq_to_label(i)]));
		// Description is wrapped in quotes for some reason, so remove them.
		let desc = r['Scientific name'].slice(1, -1);
		return {
			description: desc,
			radiance: radiances
			};
	});
	return data
}

function load_sample(idx) {
	let margin = {top:40, right: 40, bottom: 50, left: 70};
	let svg = d3.select("svg");
	let pxX = svg.attr('width');
	let pxY = svg.attr('height');
	let width = pxX - margin.right - margin.left;
	let height = pxY - margin.top - margin.bottom;

	let line1_data = data[idx].radiance;

	// Scales
	let scX = d3.scaleLinear()
		.domain([lowFreq, highFreq])
		.range([0, width]);
	let scY = d3.scaleLinear()
		//.domain(d3.extent(line1_data))
		.domain([0, 1.0])
		.range([height, 0]);

	let drawSpectrum = function(g) {
		// Line
		let lineMaker = d3.line()
			.x((_,i) => scX(freqs[i]))
			.y(d => scY(d));
		/*g.append('path')
			.attr('fill', 'none').attr('stroke', 'cyan')
			.attr('d', lineMaker(line1_data));
		*/

		// Points
		g.selectAll('circle')
			.data(line1_data).enter()
			.append('circle')
			.attr('r', 2)
			.attr('cx', (_,i) => scX(freqs[i]))
			.attr('cy', d => scY(d));
		};

	// Clear
	d3.select('svg').selectAll('*').remove();

	let figG = svg.append('g');
	let g1 = figG.append('g');
	drawSpectrum(g1);
	let axMkr1 = d3.axisLeft(scY);
	let axMkr2 = d3.axisBottom(scX);
	axMkr1(figG.append('g'));
	figG.append('g').call(axMkr2)
		.attr('transform', 'translate(0,' + height +')');
	figG.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

	// Title
	let titleG = svg.append('g')
		.attr('transform', 'translate(' + (width/2 + margin.left) + ', 20)')
		.style('text-anchor', 'middle');
	titleG.append('text').text('Reflectance Spectrum');

	// x axes title
	let titleX = svg.append('g')
		.attr('transform', 'translate(' + (width/2 + margin.left) + ',' + 
			(height + margin.top + 40)  + ')')
		.style('text-anchor', 'middle');
	titleX.append('text').text('Wavelength (nm)');


	// y axes title
	let titleY = svg.append('text')
		.attr('transform', 'rotate(-90)')
		.attr('x', 0 - (height/2) - margin.top)
		.attr('y', 30)
		.style('text-anchor', 'middle')
		.text('Reflectance');

}


getData().then(function(result) {
	data = result;
	load_sample(sample_idx);
	});


/*function set_sample(idx) {
	sample_idx = idx;*/
function set_sample(idx) {
	sample_idx = idx;
	load_sample(sample_idx);
}
</script>




<div class="specimen-imgs">
{#each {length: NUM_IMAGES} as _, i}
<img on:click={() => set_sample(i)} src="data/img/{i}.png"/>
{/each}
</div>

<div class="chosen-specimen">
<p>{data[sample_idx].description}</p>
<img src="data/img/{sample_idx}.png"/>
</div>

<svg id="fig1" width="600" height="300" style="background: lightgrey">
</svg>


<style>
div.specimen-imgs {
	max-height: 400px;
	overflow-y: scroll;
	margin: 2rem 0 2rem 0;
}

div.specimen-imgs img {
	width: 32px;
	height: 32px;
	display: inline;
}

div.chosen-specimen {
	text-align: center;
}

div.chosen-specimen img {
	display: block;
	margin: 2rem auto;
}
</style>
