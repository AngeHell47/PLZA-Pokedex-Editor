import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import os, shutil
from lib.plaza.crypto import SwishCrypto, HashDB
from lib.plaza.types import PokedexSaveDataAccessor
from lib.plaza.types.accessors import HashDBKeys

save_file_magic = bytes([0x17, 0x2D, 0xBB, 0x06, 0xEA])

POKEMON_DATA = {
    1:"Bulbasaur",2:"Ivysaur",3:"Venusaur",4:"Charmander",5:"Charmeleon",
    6:"Charizard",7:"Squirtle",8:"Wartortle",9:"Blastoise",13:"Weedle",
    14:"Kakuna",15:"Beedrill",16:"Pidgey",17:"Pidgeotto",18:"Pidgeot",
    23:"Ekans",24:"Arbok",25:"Pikachu",26:"Raichu",35:"Clefairy",36:"Clefable",
    63:"Abra",64:"Kadabra",65:"Alakazam",66:"Machop",67:"Machoke",68:"Machamp",
    69:"Bellsprout",70:"Weepinbell",71:"Victreebel",79:"Slowpoke",80:"Slowbro",
    92:"Gastly",93:"Haunter",94:"Gengar",95:"Onix",115:"Kangaskhan",
    120:"Staryu",121:"Starmie",123:"Scyther",127:"Pinsir",129:"Magikarp",
    130:"Gyarados",133:"Eevee",134:"Vaporeon",135:"Jolteon",136:"Flareon",
    142:"Aerodactyl",147:"Dratini",148:"Dragonair",149:"Dragonite",150:"Mewtwo",
    152:"Chikorita",153:"Bayleef",154:"Meganium",158:"Totodile",159:"Croconaw",
    160:"Feraligatr",167:"Spinarak",168:"Ariados",172:"Pichu",173:"Cleffa",
    179:"Mareep",180:"Flaaffy",181:"Ampharos",196:"Espeon",197:"Umbreon",
    199:"Slowking",208:"Steelix",212:"Scizor",214:"Heracross",225:"Delibird",
    227:"Skarmory",228:"Houndour",229:"Houndoom",246:"Larvitar",247:"Pupitar",
    248:"Tyranitar",280:"Ralts",281:"Kirlia",282:"Gardevoir",302:"Sableye",
    303:"Mawile",304:"Aron",305:"Lairon",306:"Aggron",307:"Meditite",
    308:"Medicham",309:"Electrike",310:"Manectric",315:"Roselia",318:"Carvanha",
    319:"Sharpedo",322:"Numel",323:"Camerupt",333:"Swablu",334:"Altaria",
    353:"Shuppet",354:"Banette",359:"Absol",361:"Snorunt",362:"Glalie",
    371:"Bagon",372:"Shelgon",373:"Salamence",374:"Beldum",375:"Metang",
    376:"Metagross",406:"Budew",407:"Roserade",427:"Buneary",428:"Lopunny",
    443:"Gible",444:"Gabite",445:"Garchomp",447:"Riolu",448:"Lucario",
    449:"Hippopotas",450:"Hippowdon",459:"Snover",460:"Abomasnow",470:"Leafeon",
    471:"Glaceon",475:"Gallade",478:"Froslass",498:"Tepig",499:"Pignite",
    500:"Emboar",504:"Patrat",505:"Watchog",511:"Pansage",512:"Simisage",
    513:"Pansear",514:"Simisear",515:"Panpour",516:"Simipour",529:"Drilbur",
    530:"Excadrill",531:"Audino",543:"Venipede",544:"Whirlipede",545:"Scolipede",
    551:"Sandile",552:"Krokorok",553:"Krookodile",559:"Scraggy",560:"Scrafty",
    568:"Trubbish",569:"Garbodor",582:"Vanillite",583:"Vanillish",584:"Vanilluxe",
    587:"Emolga",602:"Tynamo",603:"Eelektrik",604:"Eelektross",607:"Litwick",
    608:"Lampent",609:"Chandelure",618:"Stunfisk",650:"Chespin",651:"Quilladin",
    652:"Chesnaught",653:"Fennekin",654:"Braixen",655:"Delphox",656:"Froakie",
    657:"Frogadier",658:"Greninja",659:"Bunnelby",660:"Diggersby",661:"Fletchling",
    662:"Fletchinder",663:"Talonflame",664:"Scatterbug",665:"Spewpa",666:"Vivillon",
    667:"Litleo",668:"Pyroar",669:"Flabébé",670:"Floette",671:"Florges",672:"Skiddo",
    673:"Gogoat",674:"Pancham",675:"Pangoro",676:"Furfrou",677:"Espurr",678:"Meowstic",
    679:"Honedge",680:"Doublade",681:"Aegislash",682:"Spritzee",683:"Aromatisse",
    684:"Swirlix",685:"Slurpuff",686:"Inkay",687:"Malamar",688:"Binacle",689:"Barbaracle",
    690:"Skrelp",691:"Dragalge",692:"Clauncher",693:"Clawitzer",694:"Helioptile",
    695:"Heliolisk",696:"Tyrunt",697:"Tyrantrum",698:"Amaura",699:"Aurorus",
    700:"Sylveon",701:"Hawlucha",702:"Dedenne",703:"Carbink",704:"Goomy",
    705:"Sliggoo",706:"Goodra",707:"Klefki",708:"Phantump",709:"Trevenant",
    710:"Pumpkaboo",711:"Gourgeist",712:"Bergmite",713:"Avalugg",714:"Noibat",
    715:"Noivern",716:"Xerneas",717:"Yveltal",718:"Zygarde",719:"Diancie",
    720:"Hoopa",721:"Volcanion",780:"Drampa",870:"Falinks"
}
POKEMON_IDS = sorted(POKEMON_DATA.keys())

class PokedexEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PLZA Pokedex Editor")
        self.root.geometry("347x600")
        self.root.minsize(347, 400)
        self.root.maxsize(347, 900)
        self.root.configure(bg='#2c3e50')
        self.selected_file = None
        self.pokemon_vars = {}
        self.loaded_save_data = None
        self.create_widgets()

    def create_widgets(self):
        top_bar = tk.Frame(self.root, bg='#34495e', height=56)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        tk.Label(
            top_bar, text="PLZA Pokedex Editor",
            font=('Arial', 15, 'bold'), bg='#34495e', fg='#ecf0f1'
        ).pack(side=tk.LEFT, padx=12, pady=12)
        self.status_label = tk.Label(
            top_bar, text="No file loaded",
            font=('Arial', 9), bg='#34495e', fg='#95a5a6'
        )
        self.status_label.pack(side=tk.RIGHT, padx=12)
        toolbar = tk.Frame(self.root, bg='#2c3e50')
        toolbar.pack(fill=tk.X, padx=8, pady=(8, 6))
        left = tk.Frame(toolbar, bg='#2c3e50'); left.pack(side=tk.LEFT)
        tk.Button(
            left, text="Load Save", command=self.load_save,
            bg='#3498db', fg='white', font=('Arial', 9, 'bold'),
            relief='flat', padx=10, pady=5, cursor='hand2'
        ).pack(side=tk.LEFT, padx=4)
        tk.Button(
            left, text="Save Changes", command=self.save_modifications,
            bg='#27ae60', fg='white', font=('Arial', 9, 'bold'),
            relief='flat', padx=10, pady=5, cursor='hand2'
        ).pack(side=tk.LEFT, padx=4)
        opts = tk.Frame(toolbar, bg='#2c3e50'); opts.pack(side=tk.RIGHT)
        self.backup_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opts, text="Create Backup", variable=self.backup_var,
            bg='#2c3e50', fg='#ecf0f1', activebackground='#2c3e50',
            activeforeground='#ecf0f1', selectcolor='#2c3e50',
            font=('Arial', 9), cursor='hand2'
        ).pack(side=tk.RIGHT, padx=6)
        bulk = tk.Frame(self.root, bg='#2c3e50')
        bulk.pack(fill=tk.X, padx=8, pady=(0, 6))
        tk.Label(
            bulk, text="Bulk Actions:", bg='#2c3e50', fg='#95a5a6',
            font=('Arial', 9, 'bold')
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.all_captured_var = tk.BooleanVar()
        self.all_battled_var  = tk.BooleanVar()
        self.all_shiny_var    = tk.BooleanVar()
        tk.Checkbutton(
            bulk, text="Captured", variable=self.all_captured_var,
            command=self.toggle_all_captured, bg='#2c3e50', fg='#ecf0f1',
            selectcolor='#ffffff', activebackground='#2c3e50',
            activeforeground='#ecf0f1', font=('Arial', 9), cursor='hand2'
        ).pack(side=tk.LEFT, padx=4)
        tk.Checkbutton(
            bulk, text="Battled", variable=self.all_battled_var,
            command=self.toggle_all_battled, bg='#2c3e50', fg='#ecf0f1',
            selectcolor='#ffffff', activebackground='#2c3e50',
            activeforeground='#ecf0f1', font=('Arial', 9), cursor='hand2'
        ).pack(side=tk.LEFT, padx=4)
        tk.Checkbutton(
            bulk, text="Shiny", variable=self.all_shiny_var,
            command=self.toggle_all_shiny, bg='#2c3e50', fg='#ecf0f1',
            selectcolor='#ffffff', activebackground='#2c3e50',
            activeforeground='#ecf0f1', font=('Arial', 9), cursor='hand2'
        ).pack(side=tk.LEFT, padx=4)
        search = tk.Frame(self.root, bg='#2c3e50')
        search.pack(fill=tk.X, padx=8, pady=(0, 6))
        tk.Label(
            search, text="Search:", bg='#2c3e50', fg='#ecf0f1', font=('Arial', 9)
        ).pack(side=tk.LEFT, padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.filter_pokemon)
        entry = tk.Entry(
            search, textvariable=self.search_var, font=('Arial', 9),
            relief='flat', bg='#34495e', fg='#ecf0f1', insertbackground='#ecf0f1'
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, ipadx=6)
        self.count_label = tk.Label(
            search, text="Modified: 0", bg='#2c3e50',
            fg='#f39c12', font=('Arial', 9, 'bold')
        )
        self.count_label.pack(side=tk.RIGHT, padx=6)
        list_container = tk.Frame(self.root, bg='#34495e')
        list_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=0)
        list_container.grid_columnconfigure(0, weight=1)
        list_container.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(list_container, bg='#34495e', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview, width=14)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.pokemon_frame = tk.Frame(self.canvas, bg='#34495e')
        self._canvas_window = self.canvas.create_window((0, 0), window=self.pokemon_frame, anchor="nw")
        self.create_pokemon_list()
        def _sync_scrollregion(_=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        def _sync_width(event):
            sbw = self.scrollbar.winfo_width() or 14
            self.canvas.itemconfigure(self._canvas_window, width=max(0, event.width - sbw))
            _sync_scrollregion()
        self.pokemon_frame.bind("<Configure>", _sync_scrollregion)
        self.canvas.bind("<Configure>", _sync_width)
        def _on_mousewheel(e):
            if getattr(e, "delta", 0):
                self.canvas.yview_scroll(int(-e.delta/120), "units")
            else:
                self.canvas.yview_scroll(-3 if e.num == 4 else 3, "units")
        def _bind_wheel(_):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            self.canvas.bind_all("<Button-4>", _on_mousewheel)
            self.canvas.bind_all("<Button-5>", _on_mousewheel)
        def _unbind_wheel(_):
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        self.canvas.bind("<Enter>", _bind_wheel)
        self.canvas.bind("<Leave>", _unbind_wheel)
        bottom = tk.Frame(self.root, bg='#2c3e50')
        bottom.pack(fill=tk.X, side=tk.BOTTOM, padx=8, pady=6)
        link = tk.Label(
            bottom, text="Github Angehell47", fg="#61a8ff",
            bg='#2c3e50', cursor="hand2", font=("Arial", 9, "underline")
        )
        link.pack(side=tk.RIGHT)
        link.bind("<Button-1>", lambda _:
                  webbrowser.open_new("https://github.com/AngeHell47/PLZA-Full-Pokedex"))

    def create_pokemon_list(self):
        import tkinter.font as tkfont
        for w in self.pokemon_frame.winfo_children():
            w.destroy()
        hdr_font = tkfont.Font(family='Arial', size=8, weight='bold')
        row_font = tkfont.Font(family='Arial', size=8)
        longest_name = max(POKEMON_DATA.values(), key=len)
        NAME_COL_W = row_font.measure(longest_name) + 12
        _tmp = tk.Checkbutton(self.pokemon_frame); _tmp.update_idletasks()
        cb_w = _tmp.winfo_reqwidth(); cb_h = _tmp.winfo_reqheight(); _tmp.destroy()
        W_CAP = max(cb_w, hdr_font.measure("Captured"))
        W_BAT = max(cb_w, hdr_font.measure("Battled"))
        W_SHI = max(cb_w, hdr_font.measure("Shiny"))
        PAD_NAME_TO_CAP   = (30, 2)
        PAD_CAP_TO_BATTLE = (10, 2)
        PAD_BAT_TO_SHINY  = (20, 2)
        ROW_H = cb_h
        header = tk.Frame(self.pokemon_frame, bg='#2c3e50', height=ROW_H)
        header.pack(fill=tk.X, pady=(0,2))
        tk.Label(header, text="ID", bg='#2c3e50', fg='#95a5a6', font=hdr_font, width=4).pack(side=tk.LEFT, padx=(8,4))
        name_hdr_box = tk.Frame(header, bg='#2c3e50', width=NAME_COL_W, height=ROW_H)
        name_hdr_box.pack_propagate(False)
        name_hdr_box.pack(side=tk.LEFT, padx=(4,0))
        cn = tk.Canvas(name_hdr_box, bg='#2c3e50', highlightthickness=0, width=NAME_COL_W, height=ROW_H)
        cn.pack(fill=tk.BOTH, expand=True)
        cn.create_text(0, ROW_H//2, text="Name", fill='#95a5a6', font=hdr_font, anchor='w')
        def hdr_canvas(parent, text, width, pad):
            box = tk.Frame(parent, bg='#2c3e50', width=width, height=ROW_H)
            box.pack_propagate(False)
            box.pack(side=tk.LEFT, padx=pad)
            c = tk.Canvas(box, bg='#2c3e50', highlightthickness=0, width=width, height=ROW_H)
            c.pack(fill=tk.BOTH, expand=True)
            # centrage parfait au milieu du rectangle
            c.create_text(width//2, ROW_H//2, text=text, fill='#95a5a6', font=hdr_font, anchor='center')
        hdr_canvas(header, "Captured", W_CAP, PAD_NAME_TO_CAP)
        hdr_canvas(header, "Battled",  W_BAT, PAD_CAP_TO_BATTLE)
        hdr_canvas(header, "Shiny",    W_SHI, PAD_BAT_TO_SHINY)
        tk.Frame(header, bg='#2c3e50').pack(side=tk.LEFT, fill=tk.X, expand=True)
        for idx, pid in enumerate(POKEMON_IDS):
            row_bg = '#34495e' if idx % 2 == 0 else '#2c3e50'
            row = tk.Frame(self.pokemon_frame, bg=row_bg, height=ROW_H)
            row.pack(fill=tk.X, pady=1)
            self.pokemon_vars[pid] = {'captured': tk.BooleanVar(),
                                      'battled' : tk.BooleanVar(),
                                      'shiny'   : tk.BooleanVar()}
            for v in self.pokemon_vars[pid].values():
                v.trace_add('write', lambda *_: self.update_count())
            tk.Label(row, text=f"{pid:03d}", bg=row_bg, fg='#7f8c8d',
                     font=('Consolas', 8), width=4).pack(side=tk.LEFT, padx=(8,4))
            name_box = tk.Frame(row, bg=row_bg, width=NAME_COL_W, height=ROW_H)
            name_box.pack_propagate(False)
            name_box.pack(side=tk.LEFT, padx=(4,0))
            tk.Label(name_box, text=POKEMON_DATA[pid], bg=row_bg, fg='#ecf0f1',
                     font=row_font, anchor='w').pack(fill=tk.BOTH, expand=True)
            def cell(var, width, pad):
                box = tk.Frame(row, bg=row_bg, width=width, height=ROW_H)
                box.pack_propagate(False)
                box.pack(side=tk.LEFT, padx=pad)
                tk.Checkbutton(box, variable=var, bg=row_bg,
                               activebackground=row_bg, selectcolor='#ffffff',
                               cursor='hand2', bd=0, highlightthickness=0,
                               takefocus=False).pack(expand=True)
            cell(self.pokemon_vars[pid]['captured'], W_CAP, PAD_NAME_TO_CAP)
            cell(self.pokemon_vars[pid]['battled'],  W_BAT, PAD_CAP_TO_BATTLE)
            cell(self.pokemon_vars[pid]['shiny'],    W_SHI, PAD_BAT_TO_SHINY)
            tk.Frame(row, bg=row_bg).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pokemon_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_save(self):
        filename = filedialog.askopenfilename(
            title="Select save file",
            filetypes=[("All files", "*.*")]
        )
        if not filename: return
        try:
            with open(filename,"rb") as f: data = f.read()
            if not data.startswith(save_file_magic):
                messagebox.showerror("Error","Invalid save file format"); return
            blocks = SwishCrypto.decrypt(data)
            hash_db = HashDB(blocks)
            dex_block = hash_db[HashDBKeys.PokeDex]
            dex_accessor = PokedexSaveDataAccessor.from_bytes(dex_block.raw)
            self.loaded_save_data = dex_accessor
            self.selected_file = filename
            for pid in POKEMON_IDS:
                if not dex_accessor.is_pokedex_data_out_of_range(pid):
                    core = dex_accessor.get_pokedex_data(pid)
                    self.pokemon_vars[pid]['captured'].set(core.is_captured(0))
                    self.pokemon_vars[pid]['battled'].set(core.is_battled(0))
                    self.pokemon_vars[pid]['shiny'].set(core.is_shiny(0))
            self.status_label.config(text=f"Loaded: {os.path.basename(filename)}", fg='#2ecc71')
            messagebox.showinfo("Success","Save file loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load save file:\n{e}")

    def update_count(self):
        count = sum(1 for pid in POKEMON_IDS
                    if any(self.pokemon_vars[pid][k].get() for k in ('captured','battled','shiny')))
        self.count_label.config(text=f"Modified: {count}")

    def filter_pokemon(self, *_):
        term = self.search_var.get().lower()
        rows = [w for w in self.pokemon_frame.winfo_children() if isinstance(w, tk.Frame)][1:]
        for r in rows: r.pack_forget()
        idx = 0
        for pid in POKEMON_IDS:
            name = POKEMON_DATA[pid].lower()
            if term in name or term in f"{pid}":
                for r in rows:
                    labels = [w for w in r.winfo_children() if isinstance(w, tk.Label)]
                    if labels and f"{pid:03d}" in labels[0].cget('text'):
                        row_bg = '#34495e' if idx % 2 == 0 else '#2c3e50'
                        r.config(bg=row_bg)
                        for child in r.winfo_children():
                            if isinstance(child, (tk.Label, tk.Checkbutton)):
                                child.config(bg=row_bg, activebackground=row_bg)
                        r.pack(fill=tk.X, pady=1)
                        idx += 1
                        break

    def toggle_all_captured(self):
        v = self.all_captured_var.get()
        for pid in POKEMON_IDS: self.pokemon_vars[pid]['captured'].set(v)

    def toggle_all_battled(self):
        v = self.all_battled_var.get()
        for pid in POKEMON_IDS: self.pokemon_vars[pid]['battled'].set(v)

    def toggle_all_shiny(self):
        v = self.all_shiny_var.get()
        for pid in POKEMON_IDS: self.pokemon_vars[pid]['shiny'].set(v)

    def save_modifications(self):
        if not self.selected_file:
            messagebox.showerror("Error","Please load a save file first"); return
        selected = []
        for pid in POKEMON_IDS:
            c = self.pokemon_vars[pid]['captured'].get()
            b = self.pokemon_vars[pid]['battled'].get()
            s = self.pokemon_vars[pid]['shiny'].get()
            if c or b or s:
                selected.append({'id': pid,'is_captured': c,'is_battled': b,'is_shiny': s,'capture_count': 1})
        if not selected:
            messagebox.showwarning("Warning","No Pokemon selected"); return
        try:
            self.process_save_file(selected)
            messagebox.showinfo("Success", f"Save file updated!\n{len(selected)} Pokemon modified.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")

    def process_save_file(self, pokemon_entries):
        input_path = os.path.abspath(self.selected_file)
        in_dir = os.path.dirname(input_path)
        in_name = os.path.basename(input_path)

        output_path = os.path.join(in_dir, "main")
        backup_path = os.path.join(in_dir, in_name + "_old")

        if not os.path.exists(input_path): raise FileNotFoundError("File does not exist")
        if self.backup_var.get():
            if os.path.exists(backup_path): os.remove(backup_path)
            shutil.copy2(input_path, backup_path)

        with open(input_path,"rb") as f: data = f.read()
        if not data.startswith(save_file_magic): raise ValueError("Invalid file format")

        blocks = SwishCrypto.decrypt(data)
        hash_db = HashDB(blocks)
        dex_block = hash_db[HashDBKeys.PokeDex]
        accessor = PokedexSaveDataAccessor.from_bytes(dex_block.raw)

        for e in pokemon_entries:
            dev_no = int(e["id"])
            if accessor.is_pokedex_data_out_of_range(dev_no): continue
            core = accessor.get_pokedex_data(dev_no)
            core.set_captured(0, bool(e["is_captured"]))
            core.set_battled(0, bool(e["is_battled"]))
            core.set_shiny(0, bool(e["is_shiny"]))
            accessor.set_pokedex_data(dev_no, core)

        dex_block.change_data(accessor.to_bytes())
        encrypted = SwishCrypto.encrypt(hash_db.blocks)
        with open(output_path,"wb") as f: f.write(encrypted)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokedexEditorGUI(root)
    root.mainloop()
