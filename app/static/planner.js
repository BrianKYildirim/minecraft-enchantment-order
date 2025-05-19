const ENCHANTS = window.ENCHANTS;
const NAMES = window.NAMES;
const CURRENT_LV = Object.create(null);

function prettify(ns) {
    return NAMES[ns] || ns;
}

const form = document.getElementById('planner-form');
const itemSel = document.getElementById('item-select');
const dyn = document.getElementById('dynamic-area');
const modeBlk = document.getElementById('mode-block');
const resBlk = document.getElementById('result-block');
let curInputs = {}, desInputs = {};

itemSel.addEventListener('change', () => buildTables(itemSel.value));

function updateCalcButton() {
    const anyDesiredSelected = document.querySelector('#des-block .level-btn.selected');
    document.getElementById('calc-btn').disabled = !anyDesiredSelected;
}

function buildTables(item) {
    dyn.innerHTML = '';
    resBlk.style.display = 'none';
    if (!item) {
        modeBlk.classList.add('hidden');
        return;
    }

    const applicable = ENCHANTS.filter(([ns, m]) => m.items.includes(item));
    const curses = ['curse_of_binding', 'curse_of_vanishing'];
    const nonCurses = applicable.map(([ns]) => ns).filter(ns => !curses.includes(ns));

    const remaining = new Set(nonCurses);
    let groups = [];
    while (remaining.size) {
        const root = [...remaining][0];
        const queue = [root], group = new Set();
        while (queue.length) {
            const x = queue.pop();
            if (!remaining.has(x)) continue;
            remaining.delete(x);
            group.add(x);
            ENCHANTS.find(([n]) => n === x)[1].incompatible
                .forEach(i => remaining.has(i) && queue.push(i));
        }
        groups.push([...group]);
    }
    groups.sort((a, b) => b.length - a.length);
    curses.forEach(c => {
        if (applicable.some(([ns]) => ns === c)) groups.push([c]);
    });

    [['cur', '2. Current Enchantments'], ['des', '3. Desired Final Enchantments']]
        .forEach(([key, title]) => {
            const wrap = document.createElement('div');
            wrap.className = 'ench-container';
            if (key === 'des') {
                wrap.id = 'des-block';
                wrap.innerHTML = `<h3 class="mb-4">${title}</h3>`;
            } else {
                wrap.id = 'cur-block';
                wrap.innerHTML = `
        <div class="flex items-baseline justify-between mb-4">
          <h3 class="text-sm font-semibold m-0 leading-none">${title}</h3>
          <label class="inline-flex items-center gap-2 text-sm">
            Anvil Use Count:
            <input type="number" name="prior_work" value="0" min="0" max="39"
              class="w-16 rounded border border-slate-700 bg-slate-800
                     px-2 py-1 text-slate-100 text-center">
          </label>
        </div>`;
            }

            let stripe = 0;
            groups.forEach(group => {
                group.forEach(ns => {
                    const meta = ENCHANTS.find(([n]) => n === ns)[1];
                    const row = document.createElement('div');
                    row.className = `ench-row stripe-${stripe}`;
                    row.dataset.ns = ns;
                    row.dataset.incompat = meta.incompatible.join(',');
                    row.innerHTML = `
          <span class="ench-name">${prettify(ns)}</span>
          <div class="level-cell"></div>`;
                    const cell = row.querySelector('.level-cell');
                    const hidden = document.createElement('input');
                    hidden.type = 'hidden';
                    hidden.name = `${key}-${ns}`;
                    row.appendChild(hidden);

                    if (key === 'cur') curInputs[ns] = hidden;
                    else desInputs[ns] = hidden;

                    for (let lv = 1; lv <= meta.levelMax; lv++) {
                        const b = document.createElement('button');
                        b.type = 'button';
                        b.textContent = lv;
                        b.className = 'level-btn';
                        b.dataset.level = lv;
                        b.addEventListener('click', () => toggle(b, hidden, row));
                        cell.appendChild(b);
                    }

                    wrap.appendChild(row);
                });
                stripe = 1 - stripe;
            });

            dyn.appendChild(wrap);
        });

    modeBlk.classList.remove('hidden');
    updateCalcButton();
    refreshDesiredPanel();
}

function clearRow(r) {
    r.querySelectorAll('.level-btn.selected')
        .forEach(b => b.classList.remove('selected'));
    r.querySelector('input[type="hidden"]').value = '';
    updateCalcButton();
}

function toggle(btn, hidden, row) {
    const isCurrent = row.closest('#cur-block');
    const ns = row.dataset.ns;

    if (btn.classList.contains('selected')) {
        // deselect branch
        clearRow(row);
        if (isCurrent) CURRENT_LV[ns] = 0;
        // now re-run both disables & desired logic
        refreshDesiredPanel();
        return;
    }

    // select branch
    clearRow(row);
    btn.classList.add('selected');
    hidden.value = btn.dataset.level;
    if (isCurrent) CURRENT_LV[ns] = +btn.dataset.level;

    // clear incompatible siblings
    row.dataset.incompat.split(',').filter(Boolean)
        .forEach(i => {
            const rr = document.querySelector(`.ench-row[data-ns="${i}"]`);
            rr && clearRow(rr);
        });

    // recalc disables & desired rules
    updateDisable();
    refreshDesiredPanel();
    updateCalcButton();
}

function updateDisable() {
    const sel = new Set(
        [...document.querySelectorAll('.level-btn.selected')]
            .map(b => b.closest('.ench-row').dataset.ns)
    );
    const dis = new Set();
    sel.forEach(ns =>
        ENCHANTS.find(([n]) => n === ns)[1].incompatible
            .forEach(i => dis.add(i))
    );

    document.querySelectorAll('.ench-row').forEach(r => {
        const ns = r.dataset.ns;
        const keep = !!r.querySelector('.level-btn.selected');
        const off = (dis.has(ns) || sel.has(ns)) && !keep;
        r.classList.toggle('disabled-row', off);
        r.querySelectorAll('.level-btn').forEach(b => b.disabled = off);
    });
}

function refreshDesiredPanel() {
    // **Re-run the global disable logic for current ANY time we're re-rendering**
    updateDisable();

    // gather what current & desired ns are picked
    const curSel = new Set(
        Object.entries(CURRENT_LV)
            .filter(([, lv]) => lv > 0)
            .map(([ns]) => ns)
    );
    const desSel = new Set(
        [...document.querySelectorAll('#des-block .level-btn.selected')]
            .map(b => b.closest('.ench-row').dataset.ns)
    );

    // build a set of everything incompatible with ANY picked enchant
    const cannot = new Set();
    for (let ns of curSel) {
        ENCHANTS.find(([n]) => n === ns)[1].incompatible.forEach(i => cannot.add(i));
    }
    for (let ns of desSel) {
        ENCHANTS.find(([n]) => n === ns)[1].incompatible.forEach(i => cannot.add(i));
    }

    // now enforce desired‐panel rules
    document.querySelectorAll('#des-block .ench-row').forEach(row => {
        const ns = row.dataset.ns;
        const have = CURRENT_LV[ns] || 0;
        const btns = Array.from(row.querySelectorAll('.level-btn'));
        const isPicked = btns.some(b => b.classList.contains('selected'));

        if (!isPicked && cannot.has(ns)) {
            // totally forbidden now
            row.classList.add('disabled-row');
            btns.forEach(b => {
                b.disabled = true;
                b.style.opacity = '.25';
            });
            return;
        }

        // otherwise allow only levels > current, or if already picked keep it
        row.classList.remove('disabled-row');
        btns.forEach(b => {
            const lv = +b.dataset.level;
            if (b.classList.contains('selected')) {
                b.disabled = false;
                b.style.opacity = '';
            } else if (lv <= have) {
                b.disabled = true;
                b.style.opacity = '.25';
            } else {
                b.disabled = false;
                b.style.opacity = '';
            }
        });
    });

    updateCalcButton();
}

form.addEventListener('submit', e => {
    e.preventDefault();
    const fd = new FormData(form);
    fetch(form.action, {method: 'POST', body: fd})
        .then(r => r.redirected ? window.location = r.url : r.text())
        .then(html => {
            if (!html) return;
            resBlk.innerHTML = html;
            resBlk.style.display = 'block';
            resBlk.scrollIntoView({behavior: 'smooth'});
        });
});
